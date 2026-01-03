# FastAPI + Kafka

Sample production-oriented overview of using OpenTelemetry (OTel) 
with FastAPI producing and consuming kafka msg via topic, focused on tracing and metrics.

## Setup for FastAPI + aiokafka to monitor Kafka throttling
- Collect Python-side (via custom OTel metrics)
- Collect broker (via OTel JMX receiver)
- Combine both in Grafana to get a perfect view between Kafka client side and server

## OTEL dependencies

```py
opentelemetry-distro
opentelemetry-exporter-otlp
opentelemetry-instrumentation-fastapi
opentelemetry-instrumentation-aiokafka
```

Auto instrumentation via Dockerfile [Dockerfile](Dockerfile)

---

## Custom kafka metrics

Besides of default kafka metrics, you can create custom metrics [kafka_metrics.py](app/kafka_metrics.py)

## Docker

```dockerfile
# Building docker image
docker build --tag fastapi-msc-kafka:1.0 .

# Running docker image
docker run --name fastapi-msc-kafka -p 8001:8001 fastapi-msc-kafka:1.0

# Stoping container 
docker container stop fastapi-msc-kafka

# Removing container
docker container remove fastapi-msc-kafka

# Removing docker image
docker image remove fastapi-msc-kafka:1.0
```
---

## Kind
```
# Loading docker image into kind cluster
kind load docker-image fastapi-msc-kafka:1.0
```

---
## Kubectl (k8s)
```
# Applying k8s configs
kubectl apply -f k8s.yaml

# Checking the pods status
kubectl get pods -n applications
kubectl get pods -n applications | grep fastapi-msc-kafka

# Logging
kubectl logs -n applications deployments/fastapi-msc-kafka-deployment -f

# List service
kubectl get svc -n applications | grep fastapi-mfe

# Forwarding port for tests directly to k8s service
kubectl port-forward svc/fastapi-msc-kafka-service 8001:8001 -n applications

# Restarting deploymenty 
kubectl rollout restart deployment fastapi-msc-kafka-deployment -n applications

# Deleting k8s deployment 
kubectl delete -n applications deployments.apps fastapi-msc-kafka-deployment

```
---
## Grafana

