FROM apache/kafka:latest

# ===============================
# 1. Copy OpenTelemetry Javaagent
# ===============================
COPY otel_javaagent/opentelemetry-javaagent.jar /opt/opentelemetry-javaagent.jar
COPY otel_javaagent/kafka-custom.yaml /opt/kafka-custom.yaml

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
    KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1

# ===============================
# 3. Kafka Client Quotas (STATIC)
# ===============================
# GLOBAL throttle: every producer limited to 200 bytes/sec
# This guarantees throttle_time_ms > 0 under load
ENV KAFKA_CLIENT_QUOTA_CALLBACKS="org.apache.kafka.server.quota.ClientQuotaCallback" \
    KAFKA_CLIENT_QUOTA_CALLBACK_STATIC_BRACKETS="[{client_id: '*', producer_byte_rate: 1000}]" \
    KAFKA_QUOTA_WINDOW_NUM=1 \
    KAFKA_QUOTA_WINDOW_SIZE_SECONDS=1

# ===============================
# 4. JMX for OTEL Metrics (mandatory)
# ===============================
ENV KAFKA_JMX_OPTS="\
    -Dcom.sun.management.jmxremote \
    -Dcom.sun.management.jmxremote.authenticate=false \
    -Dcom.sun.management.jmxremote.ssl=false \
    -Dcom.sun.management.jmxremote.local.only=false \
    -Djava.rmi.server.hostname=0.0.0.0" \
    KAFKA_JMX_PORT=9999

# ===============================
# 5. OTEL Java Agent Configuration
# ===============================
ENV KAFKA_OPTS="\
  -javaagent:/opt/opentelemetry-javaagent.jar \
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
  -Dotel.javaagent.debug=fase \
  -Dotel.instrumentation.messaging.enabled=true \
  -Dotel.instrumentation.kafka-metrics.enabled=true"

# ===============================
# 6. JVM Heap Config
# ===============================
ENV KAFKA_HEAP_OPTS="-Xms1g -Xmx1g"

# base image already provides entrypoint
