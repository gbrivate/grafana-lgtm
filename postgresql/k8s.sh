#!/bin/bash
docker image remove postgres:1.0
kubectl delete -n applications deployments.apps postgres-deployment
docker build --no-cache  --tag postgres:1.0 .
kind load docker-image postgres:1.0
kubectl apply -f k8s.yaml