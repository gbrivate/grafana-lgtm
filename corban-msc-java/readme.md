## Docker
docker build --tag corban-msc-java:latest .
kind load docker-image corban-msc-java 
kubectl rollout restart deployment corban-msc-java-deployment -n corban
kubectl port-forward svc/corban-msc-java-service 8080:8080 -n corban


docker run -p 8002:8002 corban-msc-java:latest

docker build --tag corban-msc-java:latest .
kind load docker-image corban-msc-java
kubectl apply -f k8s.yaml

docker container stop java
docker container remove java
docker image remove corban-msc-java:latest
docker build --no-cache  --tag corban-msc-java:latest .
docker run -p 8080:8080 --name java --network=mynet -t corban-msc-java:latest

docker container stop java
docker container remove java
docker run -p 8080:8080 --name java --network=mynet -t corban-msc-java:latest


kubectl logs deployments/corban-msc-java-deployment -n corban


hey -n 200 -c 2 -q 1 http://localhost:8080/api/slow &&
hey -n 10 -c 1 -q 1 http://localhost:8080/api/loop?id=350
