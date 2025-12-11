FROM postgres:17-alpine

# Define build arguments for OTel configuration
ARG OTEL_EXPORTER_OTLP_ENDPOINT="http://grafana-service.monitoring.svc.cluster.local:4317"

# Define variáveis (não coloque senhas fixas em produção)
ENV POSTGRES_USER=myuser \
    POSTGRES_PASSWORD=mypassword \
    POSTGRES_DB=mydb \
    TZ=America/Sao_Paulo

COPY config/postgresql.conf.sample /usr/local/share/postgresql/postgresql.conf.sample

# --- Configure Structured Logging for Correlation ---
# This step ensures that PostgreSQL logs contain data required for trace correlation
## and configures the instance to use the custom conf file.
#RUN echo "log_destination = 'stderr'" >> /etc/postgresql/postgresql.conf \
#   && echo "logging_collector = 'on'" >> /etc/postgresql/postgresql.conf \
#   && echo "log_line_prefix = '%m [%p] trace_id=%a user=%u db=%d '" >> /etc/postgresql/postgresql.conf \
#   && echo "log_statement = 'all'" >> /etc/postgresql/postgresql.conf \
#   && echo "log_min_duration_statement = 300ms" >> /etc/postgresql/postgresql.conf \
#   && echo "shared_preload_libraries = 'pg_stat_statements'" >> /etc/postgresql/postgresql.conf