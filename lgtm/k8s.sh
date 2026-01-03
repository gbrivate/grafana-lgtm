#!/bin/bash

set -euo pipefail
clear

NAMESPACE="monitoring"
DEPLOYMENT="grafana-deployment"
LABEL_SELECTOR="app=lgtm"   # adjust if needed

docker build --no-cache --tag lgtm:1.0 .
kind load docker-image lgtm:1.0

clear
echo "Deleting deployment: $DEPLOYMENT ..."
kubectl delete -n "$NAMESPACE" deployment "$DEPLOYMENT" || true

echo "Waiting for pods to fully terminate..."

while true; do
    # Capture raw output; avoid breaking on 'No resources found'
    PODS=$(kubectl get pods -n "$NAMESPACE" -l "$LABEL_SELECTOR" --no-headers 2>/dev/null || true)

    # If empty OR contains no lines, pods are gone
    if [ -z "$PODS" ]; then
        echo "All pods terminated."
        break
    fi

    echo "Still waiting for pod termination..."
    echo "$PODS"
    sleep 5
done

echo "Applying ConfigMap..."
kubectl apply -f ./config/loki/loki-config-map.yaml
kubectl apply -f ./config/prometheus/prometheus-config-map.yaml
kubectl apply -f ./config/tempo/tempo-config-map.yaml
kubectl apply -f ./config/otel/otel-config-map.yaml

echo "Applying RBAC..."
kubectl apply -f ./config/otel/rbac-otel.yaml

echo "Applying Deployment..."
kubectl apply -f k8s.yaml




sleep 10

echo "Tailing logs..."
kubectl logs -n "$NAMESPACE" deployment/"$DEPLOYMENT" -f
