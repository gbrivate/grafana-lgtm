## Add the ingress-nginx Helm repo
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install ingress-nginx ingress-nginx/ingress-nginx \
--namespace ingress-nginx \
--create-namespace \
--set controller.admissionWebhooks.enabled=false


## force cleanup ingress-nginx
kubectl api-resources --verbs=list --namespaced=true -o name \
| xargs -n 1 kubectl get --show-kind --ignore-not-found -n ingress-nginx

kubectl get pods -n ingress-nginx
kubectl -n ingress-nginx get services
kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8080:80
kubectl get ingress -A -n ingress-nginx

kubectl logs deployments/ingress-nginx-controller -n ingress-nginx

kubectl rollout restart deployment ingress-nginx-controller -n ingress-nginx

helm uninstall ingress-nginx -n ingress-nginx
kubectl delete namespace ingress-nginx


kubectl get all -n ingress-nginx

helm install ingress-nginx ingress-nginx/ingress-nginx \
--namespace ingress-nginx \
--create-namespace \
--set controller.admissionWebhooks.enabled=false

## Install curl using the appropriate Package Manager
Base Image OS,Package Manager,Update Command,Install Command (for curl)
Debian/Ubuntu,apt or apt-get,apt-get update,apt-get install -y curl
Alpine,apk,Not required for apk add,apk add --no-cache curl
RHEL/CentOS/Fedora,yum or dnf,yum check-update (or dnf check-update),yum install -y curl (or dnf install -y curl)

1 - docker exec -it my-container /bin/bash
2 - apt-get update
3 - apt-get install -y curl

## hey test
hey -n 200 -c 50 -q 1 \
-m POST \
-H "Content-Type: application/json" \
-d '{"key": "user15", "value": "Ola mundo!! "}' \
http://localhost:8080/fastapi-kafka/produce


## docker commands
docker rmi $(docker images | grep "^<none>" | awk "{print $3}")
docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
docker images -a | grep none | awk '{ print $3; }' | xargs docker rmi --force

docker rmi $(docker images -f "dangling=true" -q)

# remove contianer stoped
docker container prune

#  delete all images
docker system prune -a -f

## stop all container
docker stop $(docker ps -a -q) && docker system prune -a -f

# stop container and remove it
docker stop $(docker ps -a -q) && docker rm $(docker ps -a -q)

# list container and it's name
docker ps -a --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"


