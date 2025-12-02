FROM apache/kafka:latest

# -------------------------------
# Copy OpenTelemetry Javaagent & custom rules
# -------------------------------
COPY otel_javaagent/opentelemetry-javaagent.jar /opt/opentelemetry-javaagent.jar
COPY otel_javaagent/kafka-custom.yaml /opt/kafka-custom.yaml

# Kafka configuration (KRaft)
ENV TZ=America/Sao_Paulo \
    KAFKA_NODE_ID=1 \
    KAFKA_PROCESS_ROLES="broker,controller" \
    KAFKA_CONTROLLER_QUORUM_VOTERS="1@localhost:9093" \
    KAFKA_LISTENERS="PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093" \
    KAFKA_ADVERTISED_LISTENERS="PLAINTEXT://kafka-service.corban.svc.cluster.local:9092" \
    KAFKA_LISTENER_SECURITY_PROTOCOL_MAP="CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT" \
    KAFKA_CONTROLLER_LISTENER_NAMES="CONTROLLER" \
    KAFKA_LOG_DIRS="/tmp/kraft-combined-logs" \
    CLUSTER_ID="MkU3OEVBNTcwNTJENDM2Qk" \
    KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
    KAFKA_PRODUCER_BYTE_RATE="10000" \
    KAFKA_CONSUMER_BYTE_RATE="10000"

# -------------------------------
# Expose JMX so OTEL / Prometheus can scrape via JMX Exporter
# -------------------------------
ENV KAFKA_JMX_OPTS="-Dcom.sun.management.jmxremote \
    -Dcom.sun.management.jmxremote.authenticate=false \
    -Dcom.sun.management.jmxremote.ssl=false \
    -Dcom.sun.management.jmxremote.local.only=false \
    -Djava.rmi.server.hostname=0.0.0.0" \
    KAFKA_JMX_PORT=9999

# -------------------------------
# Set Kafka JVM options with OTel javaagent and flags
# Put all JVM flags on one line (safer for Docker ENV)
# -------------------------------
ENV KAFKA_OPTS="-javaagent:/opt/opentelemetry-javaagent.jar \
      -Dotel.instrumentation.jmx.enabled=true \
      -Dotel.jmx.target.system=kafka-broker \
      -Dotel.jmx.config=/opt/kafka-custom.yaml \
      -Dotel.resource.attributes=service.name=kafka \
      -Dotel.exporter.otlp.endpoint=http://grafana-service.lgtm.svc.cluster.local:4318 \
      -Dotel.exporter.otlp.protocol=http/protobuf \
      -Dotel.metrics.exporter=otlp \
      -Dotel.traces.exporter=otlp \
      -Dotel.logs.exporter=otlp \
      -Dotel.metric.export.interval=5000 \
      -Dotel.javaagent.debug=true \
      -Dotel.instrumentation.kafka-metrics.enabled=true"



# Heap settings
ENV KAFKA_HEAP_OPTS="-Xms1g -Xmx1g"

# Note: the base apache/kafka image already defines entrypoint/cmd
# If you need to override or add custom start commands, do that in Compose or an entrypoint script.
