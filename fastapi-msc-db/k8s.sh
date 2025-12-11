#!/bin/bash
docker image remove fastapi-msc-db:1.0
kubectl delete -n applications deployments.apps fastapi-msc-db-deployment
docker build --no-cache  --tag fastapi-msc-db:1.0 .
kind load docker-image fastapi-msc-db:1.0
kubectl apply -f k8s.yaml