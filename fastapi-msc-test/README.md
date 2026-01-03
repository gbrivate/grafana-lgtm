# FastAPI

Sample production-oriented overview of using OpenTelemetry (OTel), focused on tracing and metrics.


## OTEL dependencies

```py
opentelemetry-distro
opentelemetry-exporter-otlp
opentelemetry-instrumentation-fastapi
```

Auto instrumentation via Dockerfile [Dockerfile](Dockerfile)

---

## Docker

```dockerfile
# Building docker image
docker build --tag fastapi-msc-test:1.0 .

# Running docker image
docker run --name fastapi-msc-test -p 8001:8001 fastapi-msc-test:1.0

# Stoping container 
docker container stop fastapi-msc-test

# Removing container
docker container remove fastapi-msc-test

# Removing docker image
docker image remove fastapi-msc-test:1.0
```
---

## Kind
```
# Loading docker image into kind cluster
kind load docker-image fastapi-msc-test:1.0
```

---
## Kubectl (k8s)
```
# Applying k8s configs
kubectl apply -f k8s.yaml

# Checking the pods status
kubectl get pods -n applications
kubectl get pods -n applications | grep fastapi-msc-test

# Logging
kubectl logs -n applications deployments/fastapi-msc-test-deployment -f

# List service
kubectl get svc -n applications | grep fastapi-mfe

# Forwarding port for tests directly to k8s service
kubectl port-forward svc/fastapi-msc-test-service 8001:8001 -n applications

# Restarting deploymenty 
kubectl rollout restart deployment fastapi-msc-test-deployment -n applications

# Deleting k8s deployment 
kubectl delete -n applications deployments.apps fastapi-msc-test-deployment
```
---


## Sign using hash and key

Just a test of signing content using hash key.

```
openssl genrsa -out private_key.pem 2048
openssl rsa -in private_key.pem -pubout -out public_key.pem
```