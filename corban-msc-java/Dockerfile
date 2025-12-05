FROM maven:3.8.4-openjdk-17-slim

WORKDIR /app

# Copy pom first to leverage Docker caching
COPY pom.xml .

# Copy full project
COPY src ./src

RUN mvn package

# Copy OTel Java Agent (make sure this file exists locally)
COPY opentelemetry-javaagent.jar /app/opentelemetry-javaagent.jar

ENV TZ=America/Sao_Paulo

# Use JAVA_TOOL_OPTIONS to inject the agent
ENV JAVA_TOOL_OPTIONS="-javaagent:/app/opentelemetry-javaagent.jar \
    -Dotel.service.name=corban-msc-java \
    -Dotel.resource.attributes=deployment.environment=dev,service.version=1.0.0 \
    -Dotel.exporter.otlp.protocol=grpc \
    -Dotel.exporter.otlp.endpoint=http://grafana:4317 \
    -Dotel.metrics.exporter=otlp \
    -Dotel.traces.exporter=otlp \
    -Dotel.logs.exporter=otlp \
    -Dotel.resource.attributes=service.version=1.0.0 \
    -Dotel.instrumentation.common.default-enabled=true \
    -Dotel.instrumentation.servlet.enabled=true \
    -Dotel.instrumentation.spring-web.enabled=true \
    -Dotel.semconv-stability.opt-in=http,span,metrics,logs \
    -Dotel.instrumentation.http.server.active-request-metrics.enabled=true \
    -Dotel.instrumentation.http.server.request-body-size.enabled=true \
    -Dotel.javaagent.debug=true \
    -Dotel.instrumentation.http-server.debug=true \
    -Dotel.instrumentation.http.server.response-body-size.enabled=true \
    -Dotel.metric.export.interval=5000 \
    -Dotel.metric.export.timeout=3000 \
    -Dotel.instrumentation.http.enabled=true \
    -Dotel.instrumentation.spring-boot.enabled=true \
    -Dotel.logs.include.stacktrace=true \
    -Dotel.logs.include.parameters=true \
    -Dotel.java.experimental.log-attributes=true \
    -Dotel.traces.sampler=parentbased_always_on \
    -Dotel.instrumentation.http.capture-headers.server.request=x-request-id,authorization \
    -Dotel.instrumentation.http.capture-headers.server.response=content-type \
    -Dotel.instrumentation.jvm-metrics.enabled=true \
    -Dotel.instrumentation.spring-boot-actuator.enabled=true"

EXPOSE 8080

# ---------------------------------------------------------
# Run the application with the agent
# ---------------------------------------------------------
CMD ["java", "-jar", "target/corban-msc-java-0.0.1-SNAPSHOT.jar"]
