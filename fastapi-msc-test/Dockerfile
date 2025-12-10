# Lightweight Python image
FROM python:3.11-slim

# Core environment variables for OpenTelemetry
ENV OTEL_SERVICE_NAME=fastapi-msc-test \
    OTEL_RESOURCE_ATTRIBUTES="service.version=1.0,deployment.environment=development,team=my-team" \
    OTEL_EXPORTER_OTLP_INSECURE=true \

#    OTEL_EXPORTER_OTLP_ENDPOINT=http://grafana-service.monitoring.svc.cluster.local:4317 \
    OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://grafana-service.monitoring.svc.cluster.local:4317 \
    OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://grafana-service.monitoring.svc.cluster.local:4317 \
    OTEL_PYTHON_LOG_CORRELATION=true \

    OTEL_METRICS_EXPORT_INTERVAL=5000 \
    TZ=America/Sao_Paulo

# OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=false \






# Workdir
WORKDIR /app

# Copy app
COPY /app .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run FastAPI with OTel auto-instrumentation
CMD ["opentelemetry-instrument", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]