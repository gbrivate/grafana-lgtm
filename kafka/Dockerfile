FROM apache/kafka:4.1.1

WORKDIR /opt

COPY otel_javaagent/opentelemetry-javaagent.jar /opt/opentelemetry-javaagent.jar
COPY otel_javaagent/metrics.yaml /opt/kafka-custom.yaml

RUN chown kafka:kafka opentelemetry-javaagent.jar kafka-custom.yaml
USER kafka

# Standard Kafka Configuration (mostly kept as is)
ENV TZ=America/Sao_Paulo \
    KAFKA_NODE_ID=1 \
    CLUSTER_ID="MkU3OEVBNTcwNTJENDM2Qk" \
    KAFKA_PROCESS_ROLES="broker,controller" \
    KAFKA_CONTROLLER_QUORUM_VOTERS="1@localhost:9093" \
    KAFKA_LISTENERS="PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093" \
    KAFKA_ADVERTISED_LISTENERS="PLAINTEXT://kafka-service.applications.svc.cluster.local:9092" \
    KAFKA_LISTENER_SECURITY_PROTOCOL_MAP="CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT" \
    KAFKA_CONTROLLER_LISTENER_NAMES="CONTROLLER" \
    KAFKA_LOG_DIRS="/tmp/kraft-combined-logs" \
    KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
    KAFKA_CLIENT_QUOTA_CALLBACK_STATIC_BRACKETS="[{client_id: '*', producer_byte_rate: 200}]"

ENV KAFKA_OPTS="-javaagent:/opt/opentelemetry-javaagent.jar \
  -Dotel.resource.attributes=service.name=kafka \
  -Dotel.exporter.otlp.endpoint=http://grafana-service.monitoring.svc.cluster.local:4317 \
  -Dotel.metrics.exporter=otlp \
  -Dotel.traces.exporter=otlp \
  -Dotel.logs.exporter=otlp \
  -Dotel.metric.export.interval=5000 \
  -Dotel.instrumentation.messaging.enabled=true \
  -Dotel.instrumentation.kafka-metrics.enabled=true \
  -Dotel.instrumentation.jmx.enabled=true \
  -Dotel.jmx.target.system=kafka-broker \
  -Dotel.jmx.config=/opt/kafka-custom.yaml \
  -Dotel.javaagent.debug=false \
  -Dcom.sun.management.jmxremote \
  -Dcom.sun.management.jmxremote.authenticate=false \
  -Dcom.sun.management.jmxremote.ssl=false \
  -Dcom.sun.management.jmxremote.local.only=false \
  -Djava.rmi.server.hostname=0.0.0.0"

ENV KAFKA_HEAP_OPTS="-Xms1g -Xmx1g"