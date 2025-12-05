## Docker
docker build --tag corban-msc-fastapi:latest .
kind load docker-image corban-msc-fastapi 
kubectl rollout restart deployment corban-msc-fastapi-deployment -n corban
kubectl port-forward svc/corban-msc-fastapi-service 8002:8002 -n corban


docker run -p 8002:8002 corban-msc-fastapi:latest

docker build --tag corban-msc-fastapi:latest .
kind load docker-image corban-msc-fastapi
kubectl apply -f k8s.yaml


docker container stop fastapi
docker container remove fastapi
docker build --no-cache  --tag corban-msc-fastapi:latest .
docker run -p 8001:8001 \
    --name fastapi \
    --network=mynet \
    -t corban-msc-fastapi:latest



kubectl logs deployments/corban-msc-fastapi-deployment -n corban


hey -n 1000 -c 1 -q 1 http://localhost:8080/fastapi/rolldice?player=gabriel
hey -n 10 -c 1 -q 1 http://localhost:8080/fastapi/slow
