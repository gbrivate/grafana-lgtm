# Lightweight Python image
FROM python:3.11-slim

# Core environment variables for OpenTelemetry
ENV OTEL_SERVICE_NAME=fastapi-msc-test \
    OTEL_LOG_LEVEL=info \
    OTEL_EXPORTER_OTLP_INSECURE=true \
    OTEL_EXPORTER_OTLP_PROTOCOL=grpc \
    OTEL_EXPORTER_OTLP_ENDPOINT=http://grafana:4317 \
    OTEL_PYTHON_LOG_CORRELATION=true \
    OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true \
    OTEL_METRICS_EXPORT_INTERVAL=5000 \
    TZ=America/Sao_Paulo

# Workdir
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Expose FastAPI port
EXPOSE 8001

# Run FastAPI with OTel auto-instrumentation
CMD ["opentelemetry-instrument", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]