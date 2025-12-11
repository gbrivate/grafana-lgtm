#!/bin/bash
docker image remove java-msc-test:1.0
kubectl delete -n applications deployments.apps java-msc-test-deployment
docker build --no-cache  --tag java-msc-test:1.0 .
kind load docker-image java-msc-test:1.0
kubectl apply -f k8s.yaml