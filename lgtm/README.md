# Grafana lgtm stack

Grafana LGTM refers to Grafana Labs’ unified observability stack, composed of four tightly integrated systems that cover the full telemetry spectrum:

### LGTM is Grafana’s opinionated observability stack:

| Letter | Component | Purpose                                    |
|----|--------|--------------------------------------------|
|L|Loki| Logs                                       |
|G|Grafana| Visualization & dashboards                 |
|T|Tempo| Distributed traces                         |
|M|Mimir| Metrics (Prometheus-compatible, long-term) |

### Reference architecture (OpenTelemetry-first)
```
Applications (Java / Spring / Kafka / FastAPI / Angular)
        |
        |  OTLP (gRPC / HTTP)
        v
OpenTelemetry Collector
        ├── metrics → Mimir
        ├── logs    → Loki
        └── traces  → Tempo
                        |
                        Grafana
```
Key principle:
- Apps never talk directly to Grafana
- Collector is the control point (filtering, batching, routing)

Build lgtm image Dockerfile using custom files via [Dockerfile](Dockerfile)

---

## Docker

```dockerfile
# Building docker image
docker build --tag lgtm:1.0 .

# Running docker image
docker run --name lgtm -p 8001:8001 lgtm:1.0

# Stoping container 
docker container stop lgtm

# Removing container
docker container remove lgtm

# Removing docker image
docker image remove lgtm:1.0
```
---

## Kind
```
# Loading docker image into kind cluster
kind load docker-image lgtm:1.0
```

---
## Kubectl (k8s)
```
# Applying k8s configs
kubectl apply -f k8s.yaml

# Checking the pods status
kubectl get pods -n monitoring
kubectl get pods -n monitoring | grep lgtm

# Logging
kubectl logs -n monitoring deployments/lgtm-deployment -f

# List service
kubectl get svc -n monitoring | grep fastapi-mfe

# Forwarding port for tests directly to k8s service
kubectl port-forward svc/lgtm-service 8001:8001 -n monitoring

# Restarting deploymenty 
kubectl rollout restart deployment lgtm-deployment -n monitoring

# Deleting k8s deployment 
kubectl delete -n monitoring deployments.apps lgtm-deployment
```