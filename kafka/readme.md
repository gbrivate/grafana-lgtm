# Kafka

docker build --no-cache -t kafka-otel:latest .
kind load docker-image kafka-otel:latest
kubectl rollout restart deployment kafka-deployment -n corban
kubectl port-forward svc/kafka-service 7071:7071 -n corban
kubectl get pods  -n corban -w
kubectl logs  deployments/kafka-deployment -n corban


docker build --no-cache -t kafka-otel:latest .
kind load docker-image kafka-otel:latest
kubectl apply -f k8s.yaml

/jmx/rules/kafka-broker.yaml


## Best recommended architecture for Kafka

Kafka JVM
├── jmx_prometheus_javaagent.jar  →  FULL Kafka metrics
└── opentelemetry-javaagent.jar   →  Traces + logs (+ minimal metrics)

Prometheus (inside grafana/otel-lgtm)
scrapes → /metrics (jmx agent)
OTEL Collector (built-in)
receives → traces/logs from OTEL agent
Grafana → visualization

This is textbook production architecture.

clear
docker container stop kafka
docker container remove kafka
docker build --no-cache  --tag kafka:1.0 .
docker run -p 8003:8003 \
    --name kafka \
    --network=mynet \
    -t kafka:1.0

## kafka config files path
/opt/kafka/config