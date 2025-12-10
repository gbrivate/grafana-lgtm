## Grafana lgtm stack
kubectl delete namespace monitoring
kubectl create namespace monitoring

docker build --no-cache --tag lgtm:1.0 .
kind load docker-image lgtm:1.0
kubectl rollout restart -n monitoring deployment grafana-deployment
kubectl port-forward -n monitoring svc/grafana-service 3000:3000 9090:9090

kubectl create namespace monitoring
kubectl delete -n monitoring deployments.apps grafana-deployment
docker build --no-cache --tag lgtm:1.0 .
kind load docker-image lgtm:1.0
kubectl apply -f k8s.yaml
kubectl port-forward -n monitoring svc/grafana-service 3000:3000 9090:9090

kubectl describe pod -n monitoring grafana-deployment-59479f8cbb-dpxrl

kubectl create namespace monitoring
kubectl apply -f k8s.yaml
kubectl logs -n monitoring deployments/grafana-deployment -f
kubectl get pods -n monitoring

clear
kubectl delete -n monitoring deployments.apps grafana-deployment
docker build --no-cache --tag lgtm:1.0 .
kind load docker-image lgtm:1.0
kubectl apply -f k8s.yaml
kubectl logs -n monitoring deployments/grafana-deployment -f | grep "Error:"


clear
docker container stop grafana
docker container remove grafana
docker image remove  lgtm:1.0
docker build --no-cache --tag lgtm:1.0 .
docker run -p 3000:3000 -p 4317:4317 -p 4318:4318 -p 4040:4040 -p 9090:9090  \
    --name grafana \
    --network=mynet \
    lgtm:1.0

## Queires tempo\\\

{status=error} | rate() by (resource.service.name)

