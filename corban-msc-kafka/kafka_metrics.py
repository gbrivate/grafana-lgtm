import time
from opentelemetry import metrics
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

# Setup the Meter
meter = metrics.get_meter("aiokafka.client.metrics")

# -----------------------------------------------------------
# Metrics Definitions (Existing)
# -----------------------------------------------------------

message_counter = meter.create_counter(
    "kafka_client_messages_total",
    description="Total number of messages processed by client",
    unit="1"

)

duration_histogram = meter.create_histogram(
    "kafka_client_duration_milliseconds",
    description="Time taken to send or receive messages",
    unit="ms"
)

message_size_histogram = meter.create_histogram(
    "kafka_client_message_size_bytes",
    description="Size of the message payload in bytes",
    unit="By"
)

message_lag_histogram = meter.create_histogram(
    "kafka_client_message_lag_seconds",
    description="Time difference between message creation (timestamp) and processing",
    unit="s"
)

error_counter = meter.create_counter(
    "kafka_client_errors_total",
    description="Total number of client-side errors",
    unit="1"
)

# -----------------------------------------------------------
# NEW METRIC: Kafka Throttling
# -----------------------------------------------------------
throttle_time_histogram = meter.create_histogram(
    "kafka_client_throttle_time_ms",
    description="Broker throttle time returned by Kafka (from ProduceResponse)",
    unit="ms"
)

# -----------------------------------------------------------
# PRODUCER WRAPPER
# -----------------------------------------------------------
class MonitoredProducer:
    """Wraps AIOKafkaProducer to add OTel metrics automatically."""
    def __init__(self, producer: AIOKafkaProducer):
        self._producer = producer

    async def start(self):
        await self._producer.start()

    async def stop(self):
        await self._producer.stop()

    async def send_and_wait(self, topic, value=None, key=None, **kwargs):
        start_time = time.time()
        status = "success"
        throttle_ms = 0

        try:
            result = await self._producer.send_and_wait(topic, value, key, **kwargs)

            # NEW: aiokafka exposes throttle_time_ms in the result metadata
            try:
                throttle_ms = getattr(result, "throttle_time_ms", 0) or 0
            except Exception:
                throttle_ms = 0

            return result

        except Exception as e:
            status = "error"
            raise e

        finally:
            duration = (time.time() - start_time) * 1000

            attrs = {
                "topic": topic,
                "direction": "producer",
                "status": status
            }

            # Existing metrics
            message_counter.add(1, attrs)
            duration_histogram.record(duration, attrs)

            # NEW: throttle metric
            throttle_time_histogram.record(throttle_ms, attrs)

    def __getattr__(self, name):
        return getattr(self._producer, name)


# -----------------------------------------------------------
# CONSUMER WRAPPER
# -----------------------------------------------------------
class MonitoredConsumer:
    """Wraps AIOKafkaConsumer with rich metrics: Size, Lag, Errors, (no consumer throttle available)."""
    def __init__(self, consumer: AIOKafkaConsumer):
        self._consumer = consumer

    async def start(self):
        await self._consumer.start()

    async def stop(self):
        await self._consumer.stop()

    async def getmany(self, *args, **kwargs):
        start_time = time.time()
        try:
            results = await self._consumer.getmany(*args, **kwargs)
            duration = (time.time() - start_time) * 1000

            for tp, messages in results.items():
                count = len(messages)
                if count > 0:
                    attrs = {
                        "topic": tp.topic,
                        "partition": str(tp.partition),
                        "direction": "consumer",
                        "group_id": self._consumer._group_id or "none"
                    }

                    # Existing metrics
                    message_counter.add(count, attrs)
                    duration_histogram.record(duration, attrs)

                    # Lag: based on last message
                    last_msg = messages[-1]
                    lag_seconds = (time.time() * 1000 - last_msg.timestamp) / 1000
                    message_lag_histogram.record(max(0, lag_seconds), attrs)

                    # Total batch size
                    total_bytes = sum(len(m.value) for m in messages if m.value)
                    message_size_histogram.record(total_bytes, attrs)

                    # NEW (not available for consumers → record 0)
                    throttle_time_histogram.record(0, attrs)

            return results

        except Exception as e:
            error_counter.add(1, {
                "direction": "consumer",
                "error_type": type(e).__name__
            })
            raise e

    async def __anext__(self):
        try:
            start_time = time.time()
            msg = await self._consumer.__anext__()
            duration = (time.time() - start_time) * 1000

            attrs = {
                "topic": msg.topic,
                "partition": str(msg.partition),
                "direction": "consumer",
                "group_id": self._consumer._group_id or "none"
            }

            message_counter.add(1, attrs)
            duration_histogram.record(duration, attrs)

            if msg.value:
                message_size_histogram.record(len(msg.value), attrs)

            lag_seconds = (time.time() * 1000 - msg.timestamp) / 1000
            message_lag_histogram.record(max(0, lag_seconds), attrs)

            # NEW: consumer throttle (not provided by aiokafka → 0)
            throttle_time_histogram.record(0, attrs)

            return msg

        except StopAsyncIteration:
            raise
        except Exception as e:
            error_counter.add(1, {
                "direction": "consumer",
                "error_type": type(e).__name__
            })
            raise e

    def __getattr__(self, name):
        return getattr(self._consumer, name)
