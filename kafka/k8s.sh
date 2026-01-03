#!/bin/bash
clear
docker image remove kafka:1.0
kubectl delete -n applications deployments.apps kafka-deployment
docker build --no-cache  --tag kafka:1.0 .
kind load docker-image kafka:1.0
kubectl apply -f k8s.yaml