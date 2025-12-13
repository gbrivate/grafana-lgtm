#!/bin/bash
docker image remove fastapi-msc-test:1.0
kubectl delete -n applications deployments.apps fastapi-msc-test-deployment
docker build --tag fastapi-msc-test:1.0 .
kind load docker-image fastapi-msc-test:1.0
kubectl apply -f k8s.yaml
sleep 5
kubectl logs  -n applications deployments/fastapi-msc-test-deployment -f