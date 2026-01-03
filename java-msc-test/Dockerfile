FROM maven:3.8.4-openjdk-17-slim AS build

WORKDIR /app
COPY pom.xml .
RUN mvn dependency:resolve

COPY src ./src
RUN mvn clean package -DskipTests

FROM eclipse-temurin:17-jre-alpine AS runtime

WORKDIR /app

COPY --from=build /app/target/java-msc-test-0.0.1-SNAPSHOT.jar /app/app.jar
COPY opentelemetry-javaagent-1.32.0.jar /app/opentelemetry-javaagent.jar

ENV JAVA_TOOL_OPTIONS="-javaagent:/app/opentelemetry-javaagent.jar"

ENV OTEL_SERVICE_NAME=java-msc-test \
    OTEL_RESOURCE_ATTRIBUTES="deployment.environment=dev,service.version=1.0.0" \
    OTEL_EXPORTER_OTLP_INSECURE=true \
    OTEL_EXPORTER_OTLP_PROTOCOL=grpc \
    OTEL_EXPORTER_OTLP_ENDPOINT=http://grafana-service.monitoring.svc.cluster.local:4317 \
    OTEL_METRICS_EXPORTER=otlp \
    OTEL_TRACES_EXPORTER=otlp \
    OTEL_LOGS_EXPORTER=otlp \
    OTEL_INSTRUMENTATION_JVM_METRICS_ENABLED=true \
    OTEL_INSTRUMENTATION_MICROMETER_ENABLED=true \
    OTEL_METRICS_TEMPORALITY_PREFERENCE=DELTA \
    OTEL_METRICS_EXEMPLAR_FILTER=TRACE_BASED \
    OTEL_INSTRUMENTATION_HTTP_SERVER_EMIT_EXPERIMENTAL_TELEMETRY=false \
    OTEL_INSTRUMENTATION_HTTP_SERVER_CAPTURE_REQUEST_HEADERS="" \
    OTEL_INSTRUMENTATION_HTTP_SERVER_CAPTURE_RESPONSE_HEADERS="" \
    OTEL_INSTRUMENTATION_RUNTIME_METRICS_ENABLED=true \
    OTEL_INSTRUMENTATION_HIKARI_ENABLED=true

# Empty header capture variables
# Leaving them empty explicitly disables header capture.
# This is correct and production-safe.
# Why ENV > JAVA_TOOL_OPTIONS
# Kubernetes and Helm overrides
# Cleaner diff between environments
# No JVM restart logic changes
# Order does not matter
# OpenTelemetry reads ENV at JVM startup before agent initialization.

# 6. Command to run the application
CMD ["java", "-jar", "app.jar"]