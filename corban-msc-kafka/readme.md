## Docker
docker build --tag corban-msc-kafka:latest .
kind load docker-image corban-msc-kafka 
kubectl rollout restart deployment corban-msc-kafka-deployment -n corban
kubectl port-forward svc/corban-msc-kafka-service 8001:8001 -n corban


docker run -p 8002:8002 corban-msc-kafka:latest

docker build --tag corban-msc-kafka:latest .
kind load docker-image corban-msc-kafka
kubectl apply -f k8s.yaml


kubectl logs deployments/corban-msc-kafka-deployment  -n corban


hey -n 1000 -c 10 -q 2 http://localhost:8002/rolldice


kubectl -n corban exec -it deploy/corban-msc-kafka-deployment -- sh
curl localhost:9464/metrics | grep kafka

