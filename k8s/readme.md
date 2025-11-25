#Architecture With Your Setup
[Kubernetes (kind)]
└── Pods → write logs to stdout
└── kind node → stores logs in /var/log/containers/*.log
└── OTEL Collector running as DaemonSet
└── send logs to grafana/otel-lgtm → Loki


# You are using:
kind → Kubernetes nodes are containers → logs are inside Docker container

grafana/otel-lgtm → single docker container containing:
Grafana
Loki
Tempo
Prometheus

OTEL Collector
So you need an extra OTEL Collector inside Kubernetes, because the LGTM collector cannot see the node logs inside Kind.

🟩 1. Install the Collector (DaemonSet)

Run this: kubectl apply -f https://github.com/open-telemetry/opentelemetry-collector-contrib/releases/latest/download/kubernetes-otel-collector.yaml
❗ But that file does NOT collect logs by default — we will fix it below.


# Collect logs from Pods using OpenTelemetry in my kind cluster.”

Then you need:

1️⃣ cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml

2️⃣ OpenTelemetry Operator
kubectl apply -f https://github.com/open-telemetry/opentelemetry-operator/releases/latest/download/opentelemetry-operator.yaml


kubectl apply -f otel-collector-config.yaml
kubectl apply -f otel-collector-daemonset.yaml

helm uninstall otel-agent -n opentelemetry
helm uninstall otel-cluster -n opentelemetry
kubectl delete clusterrole otel-agent-opentelemetry-collector -n opentelemetry
kubectl delete clusterrole otel-cluster-opentelemetry-collector -n opentelemetry
kubectl delete namespace opentelemetry


kubectl create namespace opentelemetry
helm upgrade --install otel-agent open-telemetry/opentelemetry-collector -f values-agent.yaml -n opentelemetry
helm upgrade --install otel-cluster open-telemetry/opentelemetry-collector -f values-cluster.yaml -n opentelemetry

kubectl get pods -l app.kubernetes.io/name=opentelemkuetry-collector -n opentelemetry -w

kubectl rollout restart -n opentelemetry deployment 