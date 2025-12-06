# === Stage 1: Build Environment ===
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install dependencies (ensure these are your project's dependencies)
WORKDIR /app
COPY . .

# Install packages needed for psycopg2 (PostgreSQL adapter)
#RUN apt-get update && apt-get install -y --no-install-recommends \
#    build-essential \
#    libpq-dev \
#    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Core environment variables for OpenTelemetry
ENV OTEL_SERVICE_NAME=fastapi-msc-db \
    OTEL_LOG_LEVEL=info \
    OTEL_EXPORTER_OTLP_INSECURE=true \
    OTEL_EXPORTER_OTLP_PROTOCOL=grpc \
    OTEL_EXPORTER_OTLP_ENDPOINT=http://grafana:4317 \
    OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://grafana:4317 \
    OTEL_LOGS_EXPORTER=otlp \
    OTEL_LOGS_EXPORTER_OTLP_ENDPOINT=http://grafana:4317 \
    OTEL_LOGS_EXPORTER_OTLP_PROTOCOL=grpc \
    OTEL_PYTHON_LOG_CORRELATION=true \
    OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true \
    OTEL_METRICS_EXPORT_INTERVAL=5000 \
    TZ=America/Sao_Paulo

# OTEL_EXPORTER_OTLP_ENDPOINT=http://grafana-service.lgtm.svc.cluster.local:4317 \

# Expose FastAPI port
EXPOSE 8002

# Run FastAPI with OTel auto-instrumentation
CMD ["opentelemetry-instrument", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]