FROM apache/kafka:latest

#COPY config/server-minimal.properties /opt/kafka/config/server.properties

# ===============================
# 1. Copy OpenTelemetry Javaagent
# ===============================
COPY otel_javaagent/opentelemetry-javaagent.jar /opt/opentelemetry-javaagent.jar
COPY otel_javaagent/metrics.yaml /opt/kafka-custom.yaml

# ===============================
# 2. Base Kafka Configuration (KRaft)
# ===============================
ENV TZ=America/Sao_Paulo \
    KAFKA_NODE_ID=1 \
    CLUSTER_ID="MkU3OEVBNTcwNTJENDM2Qk" \
    KAFKA_PROCESS_ROLES="broker,controller" \
    KAFKA_CONTROLLER_QUORUM_VOTERS="1@localhost:9093" \
    KAFKA_LISTENERS="PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093" \
    KAFKA_ADVERTISED_LISTENERS="PLAINTEXT://kafka:9092" \
    KAFKA_LISTENER_SECURITY_PROTOCOL_MAP="CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT" \
    KAFKA_CONTROLLER_LISTENER_NAMES="CONTROLLER" \
    KAFKA_LOG_DIRS="/tmp/kraft-combined-logs" \
    KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
    KAFKA_CLIENT_QUOTA_CALLBACK_STATIC_BRACKETS="[{client_id: '*', producer_byte_rate: 200}]"

# ------------------------------------------------------------------
# DELETE SECTION 4 entirely: KAFKA_JMX_OPTS
# ------------------------------------------------------------------

# ===============================
# 5. OTEL Java Agent Configuration (MERGED)
# ===============================
ENV KAFKA_OPTS="-javaagent:/opt/opentelemetry-javaagent.jar \
  -Dcom.sun.management.jmxremote \
  -Dcom.sun.management.jmxremote.authenticate=false \
  -Dcom.sun.management.jmxremote.ssl=false \
  -Dcom.sun.management.jmxremote.local.only=false \
  -Djava.rmi.server.hostname=0.0.0.0 \
  -Dotel.instrumentation.jmx.enabled=true \
  -Dotel.jmx.target.system=kafka-broker \
  -Dotel.jmx.config=/opt/kafka-custom.yaml \
  -Dotel.resource.attributes=service.name=kafka \
  -Dotel.exporter.otlp.endpoint=http://grafana:4318 \
  -Dotel.exporter.otlp.protocol=http/protobuf \
  -Dotel.metrics.exporter=otlp \
  -Dotel.traces.exporter=otlp \
  -Dotel.logs.exporter=otlp \
  -Dotel.metric.export.interval=5000 \
  -Dotel.javaagent.debug=false \
  -Dotel.instrumentation.messaging.enabled=true \
  -Dotel.instrumentation.kafka-metrics.enabled=true"

EXPOSE 9102

# ===============================
# 6. JVM Heap Config
# ===============================
ENV KAFKA_HEAP_OPTS="-Xms1g -Xmx1g"