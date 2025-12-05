import asyncio
import json
import random
import string
from aiokafka import AIOKafkaProducer
from kafka_metric import MonitoredProducer, throttle_time_histogram

KAFKA_BOOTSTRAP = "localhost:9092"
TOPIC = "test-topic"

# Create a big payload to exceed producer_byte_rate quotas
def make_payload(size=50000):
    return {
        "msg": ''.join(random.choices(string.ascii_letters + string.digits, k=size))
    }

async def flood_messages(n=2000):
    raw_producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP,
        client_id="corban-msc-kafka-test",
        acks="all",
        linger_ms=0,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    producer = MonitoredProducer(raw_producer)

    print("Starting producer...")
    await producer.start()

    throttle_observed = []

    for i in range(n):
        payload = make_payload()
        result = await producer.send_and_wait(TOPIC, value=payload)

        # result.throttle_time_ms is from Kafka broker
        t = getattr(result, "throttle_time_ms", 0)
        throttle_observed.append(t)

        if i % 100 == 0:
            print(f"[{i}] throttle_time_ms={t}")

    print("Stopping producer...")
    await producer.stop()

    print("\n========= SUMMARY =========")
    print(f"Total messages: {n}")
    print(f"Throttle counts (>0 ms): {sum(1 for x in throttle_observed if x > 0)}")
    print(f"Max throttle: {max(throttle_observed)} ms")

    print("\nHistogram confirming telemetry:")
    print("You should see values in Prometheus for:")
    print("    kafka_client_throttle_time_ms_bucket")
    print("    kafka_client_throttle_time_ms_sum")
    print("    kafka_client_throttle_time_ms_count")


if __name__ == "__main__":
    asyncio.run(flood_messages(2000))
