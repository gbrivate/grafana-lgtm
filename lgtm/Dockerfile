FROM grafana/otel-lgtm:0.12.0

# dashbords custom
COPY config/grafana/grafana-dashboards.yaml /otel-lgtm/grafana/conf/provisioning/dashboards/grafana-dashboards.yaml
COPY boards/ /otel-lgtm/boards/

ENV TZ=America/Sao_Paulo
