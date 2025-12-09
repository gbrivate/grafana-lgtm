## Docker
docker build --tag java-msc-test:latest .
kind load docker-image java-msc-test 
kubectl rollout restart deployment java-msc-test-deployment -n applications
kubectl port-forward svc/java-msc-test-service 8080:8080 -n applications


docker run -p 8002:8002 java-msc-test:latest

docker build --tag java-msc-test:latest .
kind load docker-image java-msc-test
kubectl apply -f k8s.yaml

docker container stop java
docker container remove java
docker image remove java-msc-test:latest
docker build --no-cache  --tag java-msc-test:latest .
docker run -p 8080:8080 --name java --network=mynet -t java-msc-test:latest

docker container stop java
docker container remove java
docker run -p 8080:8080 --name java --network=mynet -t java-msc-test:latest


kubectl logs deployments/java-msc-test-deployment -n applications


hey -n 200 -c 2 -q 1 http://localhost:8080/api/slow &&
hey -n 10 -c 1 -q 1 http://localhost:8080/api/loop?id=350
