import time
import json
import logging
from typing import Any, Dict

from opentelemetry import metrics, trace
from opentelemetry.propagate import get_global_textmap
from opentelemetry.semconv.trace import SpanAttributes

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


def _bytes_length_of_value(v: Any) -> int:
    """Return the byte length of a message payload regardless of type."""
    if v is None:
        return 0
    if isinstance(v, (bytes, bytearray)):
        return len(v)
    if isinstance(v, str):
        return len(v.encode("utf-8"))
    try:
        # try common serializer path (your code serializes to JSON by default)
        return len(json.dumps(v).encode("utf-8"))
    except Exception:
        # fallback: string representation
        return len(str(v).encode("utf-8"))


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
        LOG.debug("MonitoredProducer.send_and_wait: topic=%s key=%s", topic, str(key))
        start_time = time.perf_counter()
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
            },
        ) as span:

            # Inject trace context into Kafka headers
            carrier: Dict[str, str] = {}
            propagator.inject(carrier)

            # Convert to Kafka headers (key=str, value=bytes)
            otel_headers = [(str(k), str(v).encode("utf-8")) for k, v in carrier.items()]

            full_headers = headers + otel_headers

            try:
                # explicit keywords to match AIOKafkaProducer API and avoid positional issues
                result = await self._producer.send_and_wait(
                    topic=topic, value=value, key=key, headers=full_headers, **kwargs
                )

                # the broker may set throttle_time_ms on the produce response
                throttle_ms = int(getattr(result, "throttle_time_ms", 0) or 0)

                # record metrics (only once, with same attrs)
                attrs = {"topic": topic, "direction": "producer", "status": status}
                # message counter + size + throttle + duration recorded in finally block too - but keep per-message records here for accuracy
                message_counter.add(1, attrs)
                message_size_histogram.record(_bytes_length_of_value(value), attrs)

                LOG.info(
                        "Producer throttle detected: client_id=%s topic=%s throttle_ms=%d offset=%s partition=%s",
                        getattr(self._producer, "client_id", None),
                        topic,
                        throttle_ms,
                        getattr(result, "offset", None),
                        getattr(result, "partition", None),
                        result,
                )

                # attach details to span
                span.set_attribute(SpanAttributes.MESSAGING_KAFKA_MESSAGE_OFFSET, getattr(result, "offset", None))
                span.set_attribute(SpanAttributes.MESSAGING_KAFKA_PARTITION, getattr(result, "partition", None))

                # record duration + (if no throttle recorded earlier, record 0 once)
                duration_ms = (time.perf_counter() - start_time) * 1000
                attrs = {"topic": topic, "direction": "producer", "status": status}
                duration_histogram.record(duration_ms, attrs)
                throttle_time_histogram.record(int(throttle_ms or 0), attrs)

                return result

            except Exception as e:
                status = "error"
                span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
                error_counter.add(1, {"direction": "producer", "error_type": type(e).__name__})
                raise


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
        group_id = getattr(self._consumer, "_group_id", None) or "none"

        with tracer.start_as_current_span(
            f"kafka receive batch ({group_id})",
            kind=trace.SpanKind.CONSUMER,
            attributes={
                SpanAttributes.MESSAGING_SYSTEM: "kafka",
                SpanAttributes.MESSAGING_OPERATION: "receive",
                SpanAttributes.MESSAGING_CONSUMER_ID: group_id,
                SpanAttributes.PEER_SERVICE: "kafka",
            },
        ) as batch_span:

            start_time = time.perf_counter()

            try:
                results = await self._consumer.getmany(*args, **kwargs)
                duration_ms = (time.perf_counter() - start_time) * 1000
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
                    duration_histogram.record(duration_ms, attrs)

                    # ---- PROCESS EACH MESSAGE ----
                    for msg in messages:
                        incoming_headers = {
                            safe_decode(k): safe_decode(v) for k, v in (msg.headers or [])
                        }

                        # propagate parent context, if present
                        try:
                            parent_context = propagator.extract(incoming_headers)
                        except Exception:
                            parent_context = None

                        # use start_as_current_span with extracted context
                        if parent_context:
                            span_ctx_kwargs = {"context": parent_context}
                        else:
                            span_ctx_kwargs = {}

                        with tracer.start_as_current_span(
                            f"{tp.topic} process",
                            kind=trace.SpanKind.CONSUMER,
                            attributes={
                                SpanAttributes.MESSAGING_SYSTEM: "kafka",
                                SpanAttributes.MESSAGING_DESTINATION: tp.topic,
                                SpanAttributes.MESSAGING_OPERATION: "receive",
                                SpanAttributes.MESSAGING_MESSAGE_ID: str(msg.offset),
                                SpanAttributes.MESSAGING_KAFKA_MESSAGE_OFFSET: msg.offset,
                                SpanAttributes.MESSAGING_KAFKA_PARTITION: tp.partition,
                                SpanAttributes.MESSAGING_CONSUMER_ID: group_id,
                            },
                            **span_ctx_kwargs,
                        ) as span_msg:

                            # compute lag in seconds
                            try:
                                lag_seconds = (time.time() * 1000 - msg.timestamp) / 1000
                            except Exception:
                                lag_seconds = 0
                            message_lag_histogram.record(max(0, lag_seconds), attrs)

                            if msg.value:
                                # if value comes as bytes, take len directly
                                message_size_histogram.record(_bytes_length_of_value(msg.value), attrs)

                batch_span.set_attribute(SpanAttributes.MESSAGING_BATCH_MESSAGE_COUNT, total_messages)

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
            start = time.perf_counter()
            msg = await self._consumer.__anext__()
            duration_ms = (time.perf_counter() - start) * 1000

            group_id = getattr(self._consumer, "_group_id", None) or "none"

            incoming_headers = {safe_decode(k): safe_decode(v) for k, v in (msg.headers or [])}
            try:
                parent_context = propagator.extract(incoming_headers)
            except Exception:
                parent_context = None

            ctx_kwargs = {"context": parent_context} if parent_context else {}

            with tracer.start_as_current_span(
                f"{msg.topic} process",
                kind=trace.SpanKind.CONSUMER,
                attributes={
                    SpanAttributes.MESSAGING_SYSTEM: "kafka",
                    SpanAttributes.MESSAGING_DESTINATION: msg.topic,
                    SpanAttributes.MESSAGING_OPERATION: "receive",
                    SpanAttributes.MESSAGING_MESSAGE_ID: str(msg.offset),
                    SpanAttributes.MESSAGING_KAFKA_MESSAGE_OFFSET: msg.offset,
                    SpanAttributes.MESSAGING_KAFKA_PARTITION: msg.partition,
                    SpanAttributes.MESSAGING_CONSUMER_ID: group_id,
                },
                **ctx_kwargs,
            ):

                attrs = {
                    "topic": msg.topic,
                    "partition": str(msg.partition),
                    "direction": "consumer",
                    "group_id": group_id,
                }

                message_counter.add(1, attrs)
                duration_histogram.record(duration_ms, attrs)

                if msg.value:
                    message_size_histogram.record(_bytes_length_of_value(msg.value), attrs)

                try:
                    lag_seconds = (time.time() * 1000 - msg.timestamp) / 1000
                except Exception:
                    lag_seconds = 0
                message_lag_histogram.record(max(0, lag_seconds), attrs)

                # Do not record throttle=0 here — only record meaningful throttle values on consumer side if you have evidence
                return msg

        except StopAsyncIteration:
            raise

        except Exception as e:
            error_counter.add(1, {"direction": "consumer", "error_type": type(e).__name__})
            raise

    def __getattr__(self, name):
        return getattr(self._consumer, name)
