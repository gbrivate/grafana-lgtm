FROM grafana/otel-lgtm:0.12.0

# Optional: copy custom Grafana dashboards or configuration

#COPY grafana/defaults.ini  /otel-lgtm/grafana/conf/defaults.ini
#COPY prometheus/prometheus-original.yml /otel-lgtm/prometheus/prometheus.yml
#COPY prometheus/prometheus.yaml /otel-lgtm/prometheus.yaml
# COPY otel/otel-config-postgres.yaml /otel-lgtm/otel-config.yaml
#COPY otel/otelcol-config-export-http.yaml /otel-lgtm/otelcol-config-export-http.yaml

#COPY loki/loki-config.yaml /otel-lgtm/loki-config.yaml
#COPY tempo/tempo-config.yaml /otel-lgtm/tempo-config.yaml

# ✔️ Overwrite the actual OTEL Collector config used by the container
#COPY otel/otelcol-config-postgres.yaml /otel-lgtm/otelcol-config.yaml

#COPY config/otel/otelcol-config-k8s.yaml /otel-lgtm/otelcol-config.yaml

# dashbords custom
COPY config/grafana/grafana-dashboards.yaml /otel-lgtm/grafana/conf/provisioning/dashboards/grafana-dashboards.yaml
COPY boards/ /otel-lgtm/

ENV TZ=America/Sao_Paulo
