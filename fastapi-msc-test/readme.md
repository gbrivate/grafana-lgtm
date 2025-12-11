## Docker
docker build --tag fastapi-msc-test:latest .
kind load docker-image fastapi-msc-test 
kubectl rollout restart deployment fastapi-msc-test-deployment -n applications
kubectl port-forward svc/fastapi-msc-test-service 8002:8002 -n applications


docker run -p 8002:8002 fastapi-msc-test:latest




clear
docker image remove fastapi-msc-test:latest 
kubectl delete -n applications deployments.apps fastapi-msc-test-deployment
docker build --tag fastapi-msc-test:latest .
kind load docker-image fastapi-msc-test
kubectl apply -f k8s.yaml
kubectl logs -n applications deployments/fastapi-msc-test-deployment -f


docker container stop fastapi
docker container remove fastapi
docker build --no-cache  --tag fastapi-msc-test:latest .
docker run -p 8001:8001 \
    --name fastapi \
    --network=mynet \
    -t fastapi-msc-test:latest



kubectl logs deployments/fastapi-msc-test-deployment -n applications


hey -n 1000 -c 1 -q 1 http://localhost:8080/fastapi/rolldice?player=gabriel
hey -n 10 -c 1 -q 1 http://localhost:8080/fastapi/slow
