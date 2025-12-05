# build image
docker build --no-cache -t postgres:1.0 .
kind load docker-image postgres:latest
kubectl rollout restart deployment postgres-deployment -n corban

kubectl apply -f k8s.yaml

docker container stop postgres
docker container remove postgres
docker build --no-cache -t postgres:1.0 .
docker run -p 5432:5432 \
    --name postgres \
    --network=mynet \
    -t postgres:1.0


kubectl rollout restart deployment postgres-deployment -n corban
kubectl delete  -n corban deployment postgres-deployment

kubectl port-forward svc/postgres-service 5432:5432 -n corban
kubectl get pods  -n corban -w

kubectl logs  deployments/postgres-deployment -n corban

kubectl describe -n corban pod 
