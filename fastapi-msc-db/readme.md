## Docker
docker build --no-cache  --tag fastapi-msc-db:1.0 .
kind load docker-image fastapi-msc-db:1.0 
kubectl rollout restart deployment fastapi-msc-db-deployment -n applications
kubectl port-forward svc/fastapi-msc-db-service 8002:8002 -n applications

docker container stop fastapi-db
docker container remove fastapi-db
docker build --no-cache  --tag fastapi-msc-db:1.0 .
docker run -p 8002:8002 \
    --name fastapi-db \
    --network=mynet \
    -t fastapi-msc-db:1.0

docker run --add-host=host.docker.internal:host-gateway \
    -p 8001:8001 fastapi-msc-db:1.0



docker build --tag fastapi-msc-db:1.0 .
kind load docker-image fastapi-msc-db:1.0
kubectl apply -f k8s.yaml
kubectl get pods -n applications

kubectl logs deployments/fastapi-msc-db-deployment -n applications

hey -n 1000 -c 1 -q 1 http://localhost:8080/fastapi/rolldice?player=gabriel
hey -n 10 -c 1 -q 1 http://localhost:8080/fastapi/slow

kubectl delete -n applications deployments.apps fastapi-msc-db-deployment 