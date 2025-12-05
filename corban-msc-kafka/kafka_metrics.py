import time
import json
import logging

from opentelemetry import metrics, trace
from opentelemetry.propagate import get_global_textmap
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.context import Context

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

LOG = logging.getLogger("corban-msc-kafka")

# -----------------------------------------------------------
# Helper: safe header decoding (handles None, bytes, etc)
# -----------------------------------------------------------
def safe_decode(x):
    if isinstance(x, bytes):
        return x.decode("utf-8", errors="ignore")
    return x  # return None or str unchanged


# -----------------------------------------------------------
# OTel setup
# -----------------------------------------------------------
tracer = trace.get_tracer(__name__)
propagator = get_global_textmap()
meter = metrics.get_meter("aiokafka.client.metrics")

# -----------------------------------------------------------
# Metrics
# -----------------------------------------------------------
message_counter = meter.create_counter("kafka_client_messages_total")
duration_histogram = meter.create_histogram("kafka_client_duration_milliseconds")
message_size_histogram = meter.create_histogram("kafka_client_message_size_bytes")
message_lag_histogram = meter.create_histogram("kafka_client_message_lag_seconds")
error_counter = meter.create_counter("kafka_client_errors_total")
throttle_time_histogram = meter.create_histogram("kafka_client_throttle_time_ms")

# ===========================================================
# PRODUCER WRAPPER
# ===========================================================
class MonitoredProducer:
    def __init__(self, producer: AIOKafkaProducer):
        self._producer = producer

    async def start(self):
        await self._producer.start()

    async def stop(self):
        await self._producer.stop()

    async def send_and_wait(self, topic, value=None, key=None, headers=None, **kwargs):
        LOG.info("Send msc via wrapper")
        start_time = time.time()
        status = "success"
        throttle_ms = 0

        if headers is None:
            headers = []

        # ---- PRODUCER SPAN ----
        with tracer.start_as_current_span(
            f"{topic} send",
            kind=trace.SpanKind.PRODUCER,
            attributes={
                SpanAttributes.MESSAGING_SYSTEM: "kafka",
                SpanAttributes.MESSAGING_DESTINATION: topic,
                SpanAttributes.MESSAGING_OPERATION: "publish",
                SpanAttributes.PEER_SERVICE: "kafka",
            }
        ) as span:

            # Inject trace context into Kafka headers
            carrier = {}
            propagator.inject(carrier)

            # Convert to Kafka headers (key=str, value=bytes)
            otel_headers = [
                (k, v.encode("utf-8"))
                for k, v in carrier.items()
            ]

            full_headers = headers + otel_headers

            try:
                result = await self._producer.send_and_wait(
                    topic, value, key, headers=full_headers, **kwargs
                )


                throttle_ms = getattr(result, "throttle_time_ms", 0) or 0
                throttle_time_histogram.record(throttle_ms)
                message_size_histogram.record(len(json.dumps(value).encode("utf-8")))

                span.set_attribute(
                    SpanAttributes.MESSAGING_KAFKA_MESSAGE_OFFSET,
                    result.offset
                )
                span.set_attribute(
                    SpanAttributes.MESSAGING_KAFKA_PARTITION,
                    result.partition
                )

                return result

            except Exception as e:
                status = "error"
                span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
                raise

            finally:
                duration = (time.time() - start_time) * 1000
                attrs = {"topic": topic, "direction": "producer", "status": status}

                message_counter.add(1, attrs)
                duration_histogram.record(duration, attrs)
                throttle_time_histogram.record(throttle_ms, attrs)


    def __getattr__(self, name):
        return getattr(self._producer, name)


# ===========================================================
# CONSUMER WRAPPER
# ===========================================================
class MonitoredConsumer:
    def __init__(self, consumer: AIOKafkaConsumer):
        self._consumer = consumer

    async def start(self):
        await self._consumer.start()

    async def stop(self):
        await self._consumer.stop()

    # -------------------------------------------------------
    # getmany(): batch polling
    # -------------------------------------------------------
    async def getmany(self, *args, **kwargs):
        group_id = self._consumer._group_id or "none"

        with tracer.start_as_current_span(
            f"kafka receive batch ({group_id})",
            kind=trace.SpanKind.CONSUMER,
            attributes={
                SpanAttributes.MESSAGING_SYSTEM: "kafka",
                SpanAttributes.MESSAGING_OPERATION: "receive",
                SpanAttributes.MESSAGING_CONSUMER_ID: group_id,
                SpanAttributes.PEER_SERVICE: "kafka",
            }
        ) as batch_span:

            start_time = time.time()

            try:
                results = await self._consumer.getmany(*args, **kwargs)
                duration = (time.time() - start_time) * 1000
                total_messages = 0

                for tp, messages in results.items():
                    count = len(messages)
                    if count == 0:
                        continue

                    total_messages += count

                    attrs = {
                        "topic": tp.topic,
                        "partition": str(tp.partition),
                        "direction": "consumer",
                        "group_id": group_id,
                    }

                    message_counter.add(count, attrs)
                    duration_histogram.record(duration, attrs)

                    # ---- PROCESS EACH MESSAGE ----
                    for msg in messages:

                        incoming_headers = {
                            safe_decode(k): safe_decode(v)
                            for k, v in (msg.headers or [])
                        }

                        parent_context = propagator.extract(incoming_headers)

                        with tracer.start_span(
                            f"{tp.topic} process",
                            context=parent_context,
                            kind=trace.SpanKind.CONSUMER,
                            attributes={
                                SpanAttributes.MESSAGING_SYSTEM: "kafka",
                                SpanAttributes.MESSAGING_DESTINATION: tp.topic,
                                SpanAttributes.MESSAGING_OPERATION: "receive",
                                SpanAttributes.MESSAGING_MESSAGE_ID: str(msg.offset),
                                SpanAttributes.MESSAGING_KAFKA_MESSAGE_OFFSET: msg.offset,
                                SpanAttributes.MESSAGING_KAFKA_PARTITION: tp.partition,
                                SpanAttributes.MESSAGING_CONSUMER_ID: group_id,
                            }
                        ) as span_msg:

                            lag_seconds = (time.time() * 1000 - msg.timestamp) / 1000
                            message_lag_histogram.record(max(0, lag_seconds), attrs)

                            if msg.value:
                                message_size_histogram.record(len(msg.value), attrs)

                batch_span.set_attribute(
                    SpanAttributes.MESSAGING_BATCH_MESSAGE_COUNT,
                    total_messages
                )

                return results

            except Exception as e:
                batch_span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
                error_counter.add(1, {"direction": "consumer", "error_type": type(e).__name__})
                raise


    # -------------------------------------------------------
    # __anext__(): single message iterator
    # -------------------------------------------------------
    async def __anext__(self):
        try:
            start = time.time()
            msg = await self._consumer.__anext__()
            duration = (time.time() - start) * 1000

            group_id = self._consumer._group_id or "none"

            incoming_headers = {
                safe_decode(k): safe_decode(v)
                for k, v in (msg.headers or [])
            }
            parent_context = propagator.extract(incoming_headers)

            with tracer.start_as_current_span(
                f"{msg.topic} process",
                context=parent_context,
                kind=trace.SpanKind.CONSUMER,
                attributes={
                    SpanAttributes.MESSAGING_SYSTEM: "kafka",
                    SpanAttributes.MESSAGING_DESTINATION: msg.topic,
                    SpanAttributes.MESSAGING_OPERATION: "receive",
                    SpanAttributes.MESSAGING_MESSAGE_ID: str(msg.offset),
                    SpanAttributes.MESSAGING_KAFKA_MESSAGE_OFFSET: msg.offset,
                    SpanAttributes.MESSAGING_KAFKA_PARTITION: msg.partition,
                    SpanAttributes.MESSAGING_CONSUMER_ID: group_id
                }
            ):

                attrs = {
                    "topic": msg.topic,
                    "partition": str(msg.partition),
                    "direction": "consumer",
                    "group_id": group_id,
                }

                message_counter.add(1, attrs)
                duration_histogram.record(duration, attrs)

                if msg.value:
                    message_size_histogram.record(len(msg.value), attrs)

                lag_seconds = (time.time() * 1000 - msg.timestamp) / 1000
                message_lag_histogram.record(max(0, lag_seconds), attrs)
                throttle_time_histogram.record(0, attrs)

                return msg

        except StopAsyncIteration:
            raise

        except Exception as e:
            error_counter.add(1, {"direction": "consumer", "error_type": type(e).__name__})
            raise


    def __getattr__(self, name):
        return getattr(self._consumer, name)
