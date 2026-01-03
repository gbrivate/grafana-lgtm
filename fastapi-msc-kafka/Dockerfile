# Lightweight Python image
FROM python:3.11-slim

ENV LOG_LEVEL=info \
    TZ=America/Sao_Paulo

# Core environment variables for OpenTelemetry
ENV OTEL_SERVICE_NAME=fastapi-msc-test \
    OTEL_RESOURCE_ATTRIBUTES="service.version=1.0,deployment.environment=development,team=my-team" \
    OTEL_EXPORTER_OTLP_COMPRESSION=gzip \
    OTEL_EXPORTER_OTLP_INSECURE=true \
    OTEL_EXPORTER_OTLP_ENDPOINT=grafana-service.monitoring.svc.cluster.local:4317 \
    OTEL_LOGS_EXPORTER=none \
    OTEL_PYTHON_FASTAPI_EXCLUDED_URLS="health,metrics,healthz" \
    OTEL_TRACES_SAMPLER=parentbased_traceidratio \
    OTEL_TRACES_SAMPLER_ARG=0.05 \
    OTEL_METRIC_EXPORT_INTERVAL=15000 \
    OTEL_METRIC_EXPORT_TIMEOUT=5000

# Optional: enable and enrich Kafka instrumentation
ENV OTEL_INSTRUMENTATION_MESSAGING_CAPTURE_HEADERS=true \
    OTEL_INSTRUMENTATION_MESSAGING_CAPTURE_ATTRIBUTES=true

# Workdir
WORKDIR /app

# Copy app
COPY /app .

# Install dependencies (only if you have not declared the extra OTEL libs on requirements)
RUN pip install --no-cache-dir -r requirements.txt

# OpenTelemetry
RUN opentelemetry-bootstrap -a=install

# Run FastAPI with OTel auto-instrumentation
CMD ["opentelemetry-instrument", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]