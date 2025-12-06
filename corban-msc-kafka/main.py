import json
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from kafka_metrics import MonitoredProducer, MonitoredConsumer

app = FastAPI(title="FastAPI Kafka Demo")

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger("corban-msc-kafka")
LOG.info("API is starting up")

KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
TOPIC_NAME = "test-topic"

producer: AIOKafkaProducer | None = None


class MessageRequest(BaseModel):
    key: str | None = "default"
    value: str


@app.on_event("startup")
async def startup_event():
    global producer
    raw_producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        client_id="corban-msc-kafka",
        acks="all",
        linger_ms=0,
        max_request_size=10_485_760,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda v: v.encode("utf-8") if v else None,
    )
    # 2. Wrap it
    producer = MonitoredProducer(raw_producer)
    await producer.start()
    LOG.info("✅ Kafka Producer started")


@app.on_event("shutdown")
async def shutdown_event():
    global producer
    if producer:
        await producer.stop()
        LOG.info("🛑 Kafka Producer stopped")


@app.post("/produce")
async def produce_message(message: dict):
    global producer
    LOG.info("Producer starting")
    if not producer:
        raise HTTPException(status_code=500, detail="Producer not initialized")

    try:
        LOG.info("Getting keys")
        key = message.get("key")
        value = message.get("value", "")
        producer_key = str(key) if key is not None and key != "" else None
        producer_value = {"value": value}

        # This call is instrumented automatically
        LOG.info("Setting msg via producer")
        await producer.send_and_wait(TOPIC_NAME, value=producer_value, key=producer_key)

        LOG.info("Returnning status of producer")
        return {"status": "ok", "topic": TOPIC_NAME, "value": value}

    except Exception as e:
        LOG.error(f"Producer error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/consume")
async def consume_messages(limit: int = 5):
    LOG.info("Reading topic")

    raw_consumer = AIOKafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="fastapi-demo-group",
    )
    # 2. Wrap it
    consumer = MonitoredConsumer(raw_consumer)

    await consumer.start()
    messages = []

    try:
        batches = await consumer.getmany(timeout_ms=2000, max_records=limit)

        for tp, msgs in batches.items():
            for msg in msgs:
                messages.append({
                    "topic": msg.topic,
                    "partition": tp.partition,
                    "offset": msg.offset,
                    "key": msg.key.decode() if msg.key else None,
                    "value": msg.value,
                })
                if len(messages) >= limit:
                    break
            if len(messages) >= limit:
                break

    finally:
        await consumer.stop()

    return {"messages": messages}
