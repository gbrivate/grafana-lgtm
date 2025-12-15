#!/bin/bash

set -euo pipefail
clear

NAMESPACE="monitoring"
DEPLOYMENT="grafana-deployment"
LABEL_SELECTOR="app=lgtm"   # adjust if needed

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
kubectl apply -f config-map.yaml

echo "Applying Deployment..."
kubectl apply -f k8s.yaml

echo "Applying RBAC..."
kubectl apply -f rbac-otel.yaml


sleep 5

echo "Tailing logs..."
kubectl logs -n "$NAMESPACE" deployment/"$DEPLOYMENT" -f
