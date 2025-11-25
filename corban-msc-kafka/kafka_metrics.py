import time
from opentelemetry import metrics
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

# Setup the Meter
meter = metrics.get_meter("aiokafka.client.metrics")

# Define Metrics Definitions
# 1. Counter: Number of messages produced/consumed
message_counter = meter.create_counter(
    "kafka_client_messages_total",
    description="Total number of messages processed by client",
    unit="1"
)

# 2. Histogram: Latency (Time to send or Time to process)
duration_histogram = meter.create_histogram(
    "kafka_client_duration_milliseconds",
    description="Time taken to send or receive messages",
    unit="ms"
)

# 3. Histogram: Message Size (Payload in Bytes)
# Critical for understanding network throughput and capacity planning
message_size_histogram = meter.create_histogram(
    "kafka_client_message_size_bytes",
    description="Size of the message payload in bytes",
    unit="By"
)

# 4. UpDownCounter: Consumer Lag (Time-based)
# Measures how 'old' the message is when you receive it.
# High values = your consumer is too slow.
message_lag_histogram = meter.create_histogram(
    "kafka_client_message_lag_seconds",
    description="Time difference between message creation (timestamp) and processing",
    unit="s"
)

# 5. Counter: Specific Errors
# Helps you distinguish between 'connection errors' vs 'parsing errors'
error_counter = meter.create_counter(
    "kafka_client_errors_total",
    description="Total number of client-side errors",
    unit="1"
)

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
        try:
            # Call original method
            result = await self._producer.send_and_wait(topic, value, key, **kwargs)
            return result
        except Exception as e:
            status = "error"
            raise e
        finally:
            # Calculate duration in ms
            duration = (time.time() - start_time) * 1000

            # Record Metrics
            attrs = {"topic": topic, "direction": "producer", "status": status}
            message_counter.add(1, attrs)
            duration_histogram.record(duration, attrs)

    # Allow access to other methods of the underlying producer
    def __getattr__(self, name):
        return getattr(self._producer, name)


class MonitoredConsumer:
    """Wraps AIOKafkaConsumer with rich metrics: Size, Lag, and Errors."""
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
                    # Base Attributes
                    attrs = {
                        "topic": tp.topic,
                        "partition": str(tp.partition),
                        "direction": "consumer",
                        "group_id": self._consumer._group_id or "none"
                    }

                    # 1. Update standard counters
                    message_counter.add(count, attrs)
                    duration_histogram.record(duration, attrs)

                    # 2. Calculate Batch Metrics (Size & Lag)
                    # We calculate lag based on the *last* message in the batch (freshest)
                    last_msg = messages[-1]
                    lag_seconds = (time.time() * 1000 - last_msg.timestamp) / 1000
                    message_lag_histogram.record(max(0, lag_seconds), attrs)

                    # 3. Sum payload sizes
                    total_bytes = sum(len(m.value) for m in messages if m.value)
                    message_size_histogram.record(total_bytes, attrs)

            return results

        except Exception as e:
            # Capture generic errors during fetch
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

            # Record Standard Metrics
            message_counter.add(1, attrs)
            duration_histogram.record(duration, attrs)

            # Record Message Size
            if msg.value:
                message_size_histogram.record(len(msg.value), attrs)

            # Record Message Lag (Time since production)
            # msg.timestamp is in ms, convert to seconds
            lag_seconds = (time.time() * 1000 - msg.timestamp) / 1000
            message_lag_histogram.record(max(0, lag_seconds), attrs)

            return msg

        except StopAsyncIteration:
            raise StopAsyncIteration
        except Exception as e:
            error_counter.add(1, {
                "direction": "consumer",
                "error_type": type(e).__name__
            })
            raise e

    def __getattr__(self, name):
        return getattr(self._consumer, name)