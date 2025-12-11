# build image
docker build --no-cache -t postgres:1.0 .
kind load docker-image postgres:1.0
kubectl rollout restart deployment postgres-deployment -n applications

kubectl apply -f k8s.yaml

docker container stop postgres
docker container remove postgres
docker build --no-cache -t postgres:1.0 .
docker run -p 5432:5432 \
    --name postgres \
    --network=mynet \
    -t postgres:1.0


kubectl rollout restart deployment postgres-deployment -n applications
kubectl delete  -n applications deployment postgres-deployment

kubectl port-forward svc/postgres-service 5432:5432 -n applications
kubectl get pods  -n applications -w

kubectl logs  deployments/postgres-deployment -n applications

kubectl describe -n applications pod 
