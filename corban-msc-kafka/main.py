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

KAFKA_BOOTSTRAP_SERVERS = "kafka-service.corban.svc.cluster.local:9092"
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
    if not producer:
        raise HTTPException(status_code=500, detail="Producer not initialized")

    try:
        key = message.get("key", "default")
        value = message.get("value", "")

        # This call is instrumented automatically
        await producer.send_and_wait(TOPIC_NAME, value={"value": value}, key=key)

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
