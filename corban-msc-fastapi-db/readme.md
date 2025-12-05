## Docker
docker build --no-cache  --tag corban-msc-fastapi-db:1.0 .
kind load docker-image corban-msc-fastapi-db 
kubectl rollout restart deployment corban-msc-fastapi-db-deployment -n corban
kubectl port-forward svc/corban-msc-fastapi-db-service 8002:8002 -n corban

docker container stop fastapi-db
docker container remove fastapi-db
docker build --no-cache  --tag corban-msc-fastapi-db:1.0 .
docker run -p 8002:8002 \
    --name fastapi-db \
    --network=mynet \
    -t corban-msc-fastapi-db:1.0

docker run --add-host=host.docker.internal:host-gateway \
    -p 8001:8001 corban-msc-fastapi-db:1.0



docker build --tag corban-msc-fastapi-db:1.0 .
kind load docker-image corban-msc-fastapi-db
kubectl apply -f k8s.yaml
kubectl get pods -n corban

kubectl logs deployments/corban-msc-fastapi-db-deployment -n corban

hey -n 1000 -c 1 -q 1 http://localhost:8080/fastapi/rolldice?player=gabriel
hey -n 10 -c 1 -q 1 http://localhost:8080/fastapi/slow

kubectl delete -n corban deployments.apps corban-msc-fastapi-db-deployment 