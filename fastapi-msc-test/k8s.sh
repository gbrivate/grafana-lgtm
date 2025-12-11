#!/bin/bash
docker image remove fastapi-msc-test:latest
kubectl delete -n applications deployments.apps fastapi-msc-test-deployment
docker build --tag fastapi-msc-test:latest .
kind load docker-image fastapi-msc-test
kubectl apply -f k8s.yaml
sleep 5
kubectl logs deployments/ fastapi-msc-test:latest -n applications -f