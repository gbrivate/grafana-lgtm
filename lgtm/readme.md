## Grafana lgtm stack
kubectl delete namespace lgtm

kubectl create namespace lgtm

docker build --no-cache --tag lgtm:latest .
kind load docker-image lgtm:latest
kubectl rollout restart -n lgtm deployment grafana-deployment
kubectl port-forward -n lgtm svc/grafana-service 3000:3000 9090:9090

kubectl create namespace lgtm
docker build --no-cache --tag lgtm:latest .
kind load docker-image lgtm:latest
kubectl apply -f k8s.yaml
kubectl port-forward -n lgtm svc/grafana-service 3000:3000 9090:9090

kubectl describe pod -n lgtm grafana-deployment-59479f8cbb-dpxrl

kubectl create namespace lgtm
kubectl apply -f k8s.yaml
kubectl logs -n lgtm deployments/grafana-deployment
kubectl get pods -n lgt

docker run -p 3000:3000 lgtm:latest

## Queires tempo

{status=error} | rate() by (resource.service.name)