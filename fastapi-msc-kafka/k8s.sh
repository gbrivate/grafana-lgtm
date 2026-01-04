#!/bin/bash
clear
docker image remove fastapi-msc-kafka:1.0
kubectl delete -n applications deployments.apps fastapi-msc-kafka-deployment
docker build --no-cache  --tag fastapi-msc-kafka:1.0 .
kind load docker-image fastapi-msc-kafka:1.0
kubectl apply -f k8s.yaml
sleep 5000
kubectl logs -n applications deployments/fastapi-msc-kafka-deployment -f