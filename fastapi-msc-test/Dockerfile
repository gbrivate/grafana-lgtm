# Lightweight Python image
FROM python:3.11-slim

# Core environment variables for OpenTelemetry
ENV OTEL_SERVICE_NAME=fastapi-msc-test \
    OTEL_LOG_LEVEL=warning \
    OTEL_PYTHON_INSTRUMENTATION_FASTAPI_ENABLED=true \
    OTEL_PYTHON_INSTRUMENTATION_HTTP_ENABLED=true \
    OTEL_METRIC_EXPORT_INTERVAL=5000 \
    OTEL_METRIC_EXPORT_TIMEOUT=3000 \
    OTEL_EXPORTER_OTLP_COMPRESSION=gzip \
    OTEL_EXPORTER_OTLP_PROTOCOL=grpc \
    OTEL_EXPORTER_OTLP_INSECURE=true \
    OTEL_EXPORTER_OTLP_ENDPOINT=http://grafana-service.monitoring.svc.cluster.local:4317 \
    OTEL_PYTHON_FASTAPI_EXCLUDED_URLS="health,metrics,healthz" \
    OTEL_RESOURCE_ATTRIBUTES="service.version=1.0,deployment.environment=development,team=my-team" \
    OTEL_EXPORTER_OTLP_LOGS=false \
    OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=false \
    TZ=America/Sao_Paulo

# Workdir
WORKDIR /app

# Copy app
COPY /app .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run FastAPI with OTel auto-instrumentation
CMD ["opentelemetry-instrument", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]