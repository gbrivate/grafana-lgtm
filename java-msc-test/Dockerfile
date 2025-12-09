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

ENV JAVA_TOOL_OPTIONS="-javaagent:/app/opentelemetry-javaagent.jar \
    -Dotel.service.name=java-msc-test \
    -Dotel.resource.attributes=deployment.environment=dev,service.version=1.0.0 \
    -Dotel.exporter.otlp.insecure=true \
    -Dotel.exporter.otlp.protocol=grpc \
    -Dotel.exporter.otlp.endpoint=http://grafana-service.monitoring.svc.cluster.local:4317 \
    -Dotel.metrics.exporter=otlp \
    -Dotel.traces.exporter=otlp \
    -Dotel.logs.exporter=otlp \
    -Dotel.instrumentation.jvm-metrics.enabled=true"

# 6. Command to run the application
CMD ["java", "-jar", "app.jar"]