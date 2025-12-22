#!/bin/bash
clear
docker image remove fastapi-mfe-test:1.0
kubectl delete -n applications deployments.apps fastapi-mfe-test-deployment
docker build --tag fastapi-mfe-test:1.0 .
kind load docker-image fastapi-mfe-test:1.0
kubectl apply -f k8s.yaml
sleep 5
kubectl logs  -n applications deployments/fastapi-mfe-test-deployment -f
