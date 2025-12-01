FROM grafana/otel-lgtm:latest

# Optional: copy custom Grafana dashboards or configuration

#COPY grafana/defaults.ini  /otel-lgtm/grafana/conf/defaults.ini
COPY prometheus/prometheus.yml /otel-lgtm/prometheus/prometheus.yml
#COPY prometheus/prometheus.yaml /otel-lgtm/prometheus.yaml
COPY otel/otel-config.yaml /otel-lgtm/otel-config.yaml
#COPY otel/otelcol-config-export-http.yaml /otel-lgtm/otelcol-config-export-http.yaml

#COPY loki/loki-config.yaml /otel-lgtm/loki-config.yaml
#COPY tempo/tempo-config.yaml /otel-lgtm/tempo-config.yaml

# dashbords custom
COPY grafana/grafana-dashboards.yaml /otel-lgtm/grafana/conf/provisioning/dashboards/grafana-dashboards.yaml
COPY boards/ /otel-lgtm/

ENV TZ=America/Sao_Paulo \

    # --- Query performance ---
    GF_QUERY_CONCURRENT_QUERY_LIMIT=128 \
    GF_QUERY_TIMEOUT=5s \

    # --- Data proxy (backend → Prometheus/Loki) ---
    GF_DATAPROXY_TIMEOUT=30 \
    GF_DATAPROXY_CONCURRENT_LIMIT=512 \
    GF_DATAPROXY_KEEP_ALIVE_SECONDS=5 \

    # --- Dashboard refresh ---
    GF_DASHBOARDS_MIN_REFRESH_INTERVAL=5s \

    # --- Disable noisy logs ---
    GF_LOG_MODE=console \
    GF_LOG_FILTERS=rendering:info \

    # --- Enable query caching in Grafana (v10+) ---
    GF_FEATURE_TOGGLES_ENABLE=queryCaching \
    GF_CACHING_ENABLED=true \
    GF_CACHING_TTL=30s


EXPOSE 3000 4317 4318 9090
