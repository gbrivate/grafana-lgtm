# Complete Monitoring & Instrumentation Stack

This repository provides a **full end‑to‑end monitoring, observability, and instrumentation environment** using Kubernetes (via KinD), OpenTelemetry, and the Grafana **LGTM stack** (Loki, Grafana, Tempo, Prometheus, OTEL Collector).

It also includes multiple **sample applications** (FastAPI, FastAPI + DB, Spring Boot, Apache Kafka, PostgreSQL) deployed on Kubernetes and fully observable through OTEL.

---

## 🚀 Overview

This project brings together:

* **KinD (Kubernetes-in-Docker)** for a lightweight local Kubernetes cluster.
* **Grafana OTEL LGTM stack** using the official `grafana/otel-lgtm:latest` Docker image.
* **OpenTelemetry (OTEL)** for metrics, logs, and traces.
* **Full set of sample microservices**:

    * FastAPI
    * FastAPI + PostgreSQL
    * Spring Boot
    * Apache Kafka
    * PostgreSQL database
* **Complete Kubernetes deployment configuration**:

    * Deployments
    * Services
    * Ingress
* **All microservices exposed via an Ingress Controller**.

The purpose is to demonstrate **complete monitoring, tracing, logging, metrics, and distributed observability** for modern microservices running in a real Kubernetes cluster.

---

## 🧱 Architecture

* **KinD cluster** hosts everything locally
* **Grafana OTEL LGTM** stack provides the following:

    * **Loki** → Logs
    * **Tempo** → Traces
    * **Prometheus** → Metrics
    * **OTEL Collector** → Receives and routes telemetry data
* Each application is fully instrumented using OTEL SDK or auto-instrumentation
* Telemetry is sent to the Collector → Prometheus / Tempo / Loki
* Grafana dashboards visualize all services
* Everything is deployed using standard Kubernetes YAML

---

## 📦 Included Sample Applications

### ✔ FastAPI
Basic Python API instrumented with OpenTelemetry.

### ✔ FastAPI + PostgreSQL
API including database calls, demonstrating OTEL database instrumentation.

### ✔ Spring Boot
A Java microservice using OTEL Java Agent for auto‑instrumentation.

### ✔ Apache Kafka
Kafka broker + producers/consumers instrumented for distributed tracing.

### ✔ PostgreSQL Database
Running in a container inside the cluster.

---

## ☸️ Kubernetes Resources

Each application includes:

* **Deployment** → containers, versions, env vars
* **Service** → internal service endpoints
* **Ingress** → external route via Ingress Controller

All services are accessible through a single ingress (e.g. `http://localhost/<service>`).

---

## 📊 Monitoring & Observability

All observability signals are enabled:

### 📈 Metrics
Collected via OTEL SDK / Collector and scraped by Prometheus.

### 📂 Logs
Collected using OTEL logging exporter and stored in Loki.

### 🔍 Traces
Distributed tracing using OTLP → Tempo.

### 🖥 Dashboards
Grafana provides:

* Application dashboards
* Service maps
* Trace waterfall views
* Log aggregation views

---

## 🧰 Requirements

* Docker - builds the application image
* KinD - runs a local Kubernetes cluster using Docker
* kubectl - manages and inspects Kubernetes resources
* Helm - deploys and manages complex applications on the cluster

---

## 📝 Purpose

This repository exists to provide a **complete, ready‑to‑use local observability lab**:

* Perfect for learning OTEL
* Testing distributed tracing
* Building dashboards
* Understanding Kubernetes observability patterns
* Experimenting with multiple languages and workloads

---

## 🧭 Architecture Diagram

Below is a conceptual overview of the observability stack in this repository:

                                User / Browser (http://www...)
                                                |
                                                |
    +-------------------------------------------|-----------------------------------+
    |  KUBERNETES CLUSTER                       v                                   |
    |                                 +---------------------+                       |
    |                                 |  Ingress Controller |                       |
    |                                 +----------+----------+                       |
    |                                            |                                  |         
    |             _______________________________|_______________                   |
    |             |                                             |                   |
    |             |                                             v                   | 
    |             |                      +---------------------------------------+ |
    |             |                      |  LGTM Stack (grafana/otel-lgtm)       |  |
    |             |                      |                                       |  |
    |             |                      |  +-----------+      +--------------+  |  |
    |             |                      |  | Grafana   |<---->| Prometheus   |  |  |
    |             |                      |  | UI        |<---->| Tempo        |  |  |
    |             v                      |  +-----------+      | Loki         |  |  |
    |  +------------------------+        |                     +-------^------+  |  |
    |  | Application Workloads  |        |                             |         |  |
    |  |                        |        |                      +------+-------+ |  |
    |  | [FastAPI] [SpringBoot] |        |                      | OTEL         | |  |
    |  | [Postgres] [Kafka]     |        |                      +------+-------+ |  |
    |  | [redis]                |        +--------+--------------------^---------+  |
    |  +----------+-------------+                                      |            |
    |             |                                                    |            |
    |             +----(OTLP Telemetry: Logs, Metrics, Traces)---------+            |
    |                                                                               |
    +-------------------------------------------------------------------------------+

---

## 🧩 Folder Structure 

```
grafana-lgtm            # Root folder
│
├── fastapi-msc-db      # FastAPI app with OTEL, Sqlalchemy, Postgres.
│   ├── app/            # Python files, requirements etc.
│   ├── docker.sh       # Running container with docker only.
│   ├── Dockerfile      # Dockerfile to build image with custom OTEL setup.
│   ├── k8s.yaml        # K8s deployment/service/ingress config.
│   └── readme.md       # Readme.md for specific instructions.
│
├── fastapi-msc-kafka   # FastAPI app with OTEL, custom metric, Kafka.
│   ├── app/            # Python files, requirements etc.
│   ├── test/           # Stress test Kafak and unit test.
│   ├── docker.sh       # Running container with docker only.
│   ├── Dockerfile      # Dockerfile to build image with custom OTEL setup.
│   ├── k8s.yaml        # K8s deployment/service/ingress config.
│   └── readme.md       # Readme.md for specific instructions.
│
├── fastapi-msc-test    # FastAPI app with OTEL, custom metric.
│   ├── app/            # Python files, requirements etc.
│   ├── docker.sh       # Running container with docker only.
│   ├── Dockerfile      # Dockerfile to build image with custom OTEL setup.
│   ├── k8s.yaml        # K8s deployment/service/ingress config.
│   └── readme.md       # Readme.md for specific instructions.
│
├── java-msc-test       # Spring boot app with OTEL
│   ├── src/            # Source, controller, unit test etc.
│   ├── test/           # Stress test
│   ├── docker.sh       # Running container with docker only.
│   ├── Dockerfile      # Dockerfile to build image with custom OTEL setup.
│   ├── k8s.yaml        # K8s deployment/service/ingress config.
│   ├── opentelemetry-javaagent-1.32.0.jar # For instrumentation, there is other ways to do it using maven libs etc. 
│   └── readme.md       # Readme.md for specific instructions.
│
├── kafka               # Apache kafka
│   ├── config/         # Overwrite configs for kafka.
│   ├── otel_javaagent/ # Java Agent jar, custom kafka metris.
│   ├── docker.sh       # Running container with docker only.
│   ├── Dockerfile      # Dockerfile to build image with custom OTEL setup.
│   ├── k8s.yaml        # K8s deployment/service/ingress config. 
│   └── readme.md       # Readme.md for specific instructions.
│
├── lgtm/               # Grafana+OTEL stack
│   ├── boards/         # Custom boards.
│   ├── config/         # Overwrite default configs (grafana, loki, otel, prometheus and tempo).
│   ├── docker.sh       # Running container with docker only.
│   ├── Dockerfile      # Dockerfile to build image with custom OTEL setup.
│   ├── k8s.yaml        # K8s deployment/service/ingress config. 
│   └── readme.md       # Readme.md for specific instructions.
│
├── postgresql/         # PostgresSQL 
│   ├── boards/         # Custom boards.
│   ├── config/         # Overwrite default configs
│   ├── docker.sh       # Running container with docker only.
│   ├── Dockerfile      # Dockerfile to build image with custom OTEL setup.
│   ├── k8s.yaml        # K8s deployment/service/ingress config. 
│   └── readme.md       # Readme.md for specific instructions.
│
├── .gitignore          
├──  grafana.png        # Grafana dashboard image
├──  kind-config.yaml   # Custom kind cluster
└──  readme.md
```
---

## 🔧 Setup Guide (Step-by-Step)

### 1️⃣ Create the KinD Cluster

```
kind create cluster --config kind-config.yaml
## After cluster created, run "kubectl get pods -ALL" you should get these pods running
NAMESPACE            NAME                                         READY   STATUS    RESTARTS   AGE  
kube-system          coredns-668d6bf9bc-9dcmg                     1/1     Running   0          47s   
kube-system          coredns-668d6bf9bc-g2ck6                     1/1     Running   0          47s
kube-system          etcd-kind-control-plane                      1/1     Running   0          52s
kube-system          kindnet-ttcz2                                1/1     Running   0          47s
kube-system          kube-apiserver-kind-control-plane            1/1     Running   0          52s
kube-system          kube-controller-manager-kind-control-plane   1/1     Running   0          52s
kube-system          kube-proxy-j6cdq                             1/1     Running   0          47s
kube-system          kube-scheduler-kind-control-plane            1/1     Running   0          52s
local-path-storage   local-path-provisioner-58cc7856b6-csxxx      1/1     Running   0          47s
```

### Kubernetes System Pods Overview

This document explains the purpose of common system Pods found in a Kubernetes cluster, particularly in a **kind (Kubernetes in Docker)** environment.

### System Pods and Their Purpose

| Pod | Purpose |
|----|--------|
| `coredns` | Provides internal DNS and service discovery so Pods can resolve Services by name |
| `etcd` | Distributed key-value store that holds the entire cluster state |
| `kube-apiserver` | Entry point for all Kubernetes API requests (`kubectl`, controllers, schedulers) |
| `kube-controller-manager` | Runs control loops that reconcile desired state with actual state |
| `kube-scheduler` | Selects the most suitable Node for newly created Pods |
| `kube-proxy` | Implements Service networking and traffic routing to Pods |
| `kindnet` | CNI plugin responsible for Pod-to-Pod networking in kind clusters |
| `local-path-provisioner` | Dynamically provisions local PersistentVolumes for development clusters |

### Notes

- Most of these Pods run in the `kube-system` namespace.
- These components are critical for cluster operation and are usually managed automatically.
- In managed Kubernetes services (EKS, GKE, AKS), some of these components are hidden from users.
- `local-path-provisioner` is intended for **local development**, not production workloads.

### Mental Model

- **etcd** → Cluster memory
- **kube-apiserver** → API gateway
- **scheduler** → Placement decision-maker
- **controllers** → State reconciliation engines
- **kube-proxy / CNI** → Networking layer
- **CoreDNS** → Service name resolution

---

### 2️⃣ Install NGINX Ingress Controller

```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.11.0/deploy/static/provider/kind/deploy.yaml
```

Wait for it:

```
kubectl get pods -n ingress-nginx
NAME                                        READY   STATUS      RESTARTS   AGE
ingress-nginx-admission-create-th4m7        0/1     Completed   0          97s
ingress-nginx-admission-patch-cjlv4         0/1     Completed   2          97s
ingress-nginx-controller-77cdd96884-qcmb2   1/1     Running     0          97s
```

Test http://localhost you should get "404 Not Found nginx" from nginx controller setup, which is ok.
Before we instrument k8s, let's deploy a simple FastAPI app with some endpoints and expose it via ingress controller.

### 3️⃣ Deploying LGTM (Grafana + OTEL)

We are going to use this docker image 'grafana/otel-lgtm:0.12.0' which has all ini one, nice to run locally (not production setup):
```
OpenTelemetry collector => for receiving OpenTelemetry data.
Prometheus              => metrics database.
Tempo                   => trace database.
Loki                    => logs database.
Grafana                 => for visualization.
```
# LGTM Embedded Service Endpoints

The **grafana/otel-lgtm** container bundles multiple observability backends.  
Inside the container, each embedded service listens on the following local endpoints.

## Signal Endpoints

| Signal   | Backend      | Protocol        | Endpoint |
|----------|--------------|-----------------|----------|
| Traces   | Tempo        | OTLP HTTP       | `http://127.0.0.1:4318` |
| Traces   | Tempo        | OTLP gRPC       | `127.0.0.1:4317` |
| Metrics  | Prometheus   | OTLP HTTP       | `http://127.0.0.1:9090/api/v1/otlp` |
| Metrics  | Prometheus   | Remote Write    | `http://127.0.0.1:9090/api/v1/write` |
| Logs     | Loki         | OTLP HTTP       | `http://127.0.0.1:3100/otlp` |
| Profiles | Pyroscope    | OTLP gRPC       | `127.0.0.1:4040` |
| UI       | Grafana      | HTTP            | `http://127.0.0.1:3000` |


Building and deployment into k8s, at this moment we are not applying Otel custom configs yet.

```
# Building docker image and loading it into kind cluster
cd lgtm
docker build --no-cache --tag lgtm:1.0 .

# It may take some time given the image size.
kind load docker-image lgtm:1.0  

# Create a k8s namespace 'monitoring', it's important create namespace and keep things separated
kubectl create namespace monitoring

# Applying k8s configs
kubectl apply -f k8s.yaml

# Verify if pod is runing
kubectl get -n monitoring pods
NAME                                  READY   STATUS    RESTARTS   AGE
grafana-deployment-8458dd4b69-k27x9   1/1     Running   0          15s
```
** In order to run all of this commands above once, there is k8s.sh, but it's recommended run one by one first time.

Open browser at http://localhost/grafana (admim/admin) then you should see that:

![Grafana home page](grafana.png)

So far we got running:

- K8s cluster running via Kind
- Ingress controller via Kind
- Grafana lgtm stack (Grafana, Tempo, Loki, Promehtues(Mimir built on) amd Open telemetry - Otel)

With all tools in place, let's instrument it all.

## There Two-level visibility:

- Application observability → what happens within your code (business logic, requests, errors).
- Platform observability → what happens around your code (Kubernetes, network, resources, infrastructure).

You don't need to choose between instrumenting Kubernetes or an application;
ideally, you should combine both, each with a specific purpose.
- Logs - getting from k8s instrumentation (of course metrics of k8s is also here).
- Metrics/traces - getting from app via OTE.


## K8s Instrumentation

One of the best way to instrument Kubernetes (K8s) using OpenTelemetry (Otel) for collecting logs, traces, and metrics is by leveraging the OpenTelemetry Operator combined with the OpenTelemetry Collector.

This approach:
- Centralizes configuration
- Automates collection
- Separates the concerns of data collection from application code, which is ideal for a dynamic container environment like Kubernetes.


Let's clarify some understanding.

- Pods → write logs to stdout
- kind node → stores logs in /var/log/containers/*.log
- OTEL collects logs/metrics from Kind node.
- OTEL Sends logs to grafana/otel-lgtm → Loki

In order to get these info from K8s we will need install some packages:

* Cert-manager (Only if you want to enforce security data traffic via TLS etc)
* OpenTelemetry Operator (may need cert-manager or not)
* kube-state-metrics

By default, the OpenTelemetry Operator expects cert-manager to be present to issue certificates for its admission webhooks.

Add cert-manager later only if you need:
- Admission webhooks enabled
- mTLS between collectors
- Production-like security testing

### Do you need both (OpenTelemetry Operator and kube-state-metrics)?

Yes, in most real setups. They are **complementary**, not overlapping.

### Telemetry coverage

| Telemetry type              | OpenTelemetry Operator | kube-state-metrics |
|----------------------------|------------------------|--------------------|
| Application logs           | ✅                     | ❌                 |
| Application metrics        | ✅                     | ❌                 |
| Traces                     | ✅                     | ❌                 |
| Pod / Deployment state     | ⚠️ (indirect)          | ✅                 |
| HPA / rollout visibility   | ❌                     | ✅                 |
| Kubernetes metadata        | ❌                     | ✅                 |

- **OpenTelemetry Operator** → *How your applications behave*
- **kube-state-metrics** → *What Kubernetes is doing*


### Installing OpenTelemetry Operator with cert-manager 

```
helm repo add jetstack https://charts.jetstack.io
helm repo update

helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --set installCRDs=true
```

Installing Opentelemetry Operator

```
# Add the Helm repository
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
helm repo update

helm install otel-operator open-telemetry/opentelemetry-operator \
  --namespace opentelemetry-operator-system \
  --create-namespace
```

### Installing OpenTelemetry Operator (without Cert-manager)
```
# In case any trouble  uninstall and install again.
helm uninstall otel-operator -n opentelemetry-operator-system

# Install wihtout cert-manager
helm install otel-operator open-telemetry/opentelemetry-operator \
  --namespace opentelemetry-operator-system \
  --create-namespace \
  --set admissionWebhooks.create=false \
  --set-string manager.env.ENABLE_WEBHOOKS=false
```
  
```
# Verify the instalation
 kubectl get pods -n opentelemetry-operator-system
NAME                                                    READY   STATUS    RESTARTS   AGE
otel-operator-opentelemetry-operator-7f55bcdbff-d4t5z   2/2     Running   0          23s
```

### Installing kube-state-metrics
```
# Adding repo  via Helm (recommend)
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Instalar kube-state-metrics
helm install ksm prometheus-community/kube-state-metrics \
--namespace kube-system \
--create-namespace

# Verify the instalations
kubectl get all -A -l app.kubernetes.io/name=kube-state-metrics
NAMESPACE     NAME                                         READY   STATUS    RESTARTS   AGE
kube-system   pod/ksm-kube-state-metrics-8c88554fd-4bvfb   1/1     Running   0          2m23s

NAMESPACE     NAME                             TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
kube-system   service/ksm-kube-state-metrics   ClusterIP   10.96.206.230   <none>        8080/TCP   2m23s

NAMESPACE     NAME                                     READY   UP-TO-DATE   AVAILABLE   AGE
kube-system   deployment.apps/ksm-kube-state-metrics   1/1     1            1           2m23s

NAMESPACE     NAME                                               DESIRED   CURRENT   READY   AGE
kube-system   replicaset.apps/ksm-kube-state-metrics-8c88554fd   1         1         1       2m23s
```

So far we have this setup

```
# List all recourses of k8s "kubectl get all -A"
NAMESPACE                       NAME                                                        READY   STATUS      RESTARTS       AGE
ingress-nginx                   pod/ingress-nginx-admission-create-57kj2                    0/1     Completed   0              3h16m
ingress-nginx                   pod/ingress-nginx-admission-patch-tmzsl                     0/1     Completed   2              3h16m
ingress-nginx                   pod/ingress-nginx-controller-77cdd96884-f2mqn               1/1     Running     0              3h16m
kube-system                     pod/coredns-668d6bf9bc-mgmxv                                1/1     Running     0              3h17m
kube-system                     pod/coredns-668d6bf9bc-xbx74                                1/1     Running     0              3h17m
kube-system                     pod/etcd-kind-control-plane                                 1/1     Running     0              3h17m
kube-system                     pod/kindnet-6ftmp                                           1/1     Running     0              3h17m
kube-system                     pod/ksm-kube-state-metrics-8c88554fd-4bvfb                  1/1     Running     0              3m22s
kube-system                     pod/kube-apiserver-kind-control-plane                       1/1     Running     0              3h17m
kube-system                     pod/kube-controller-manager-kind-control-plane              1/1     Running     2 (3h4m ago)   3h17m
kube-system                     pod/kube-proxy-jnv7t                                        1/1     Running     0              3h17m
kube-system                     pod/kube-scheduler-kind-control-plane                       1/1     Running     2 (3h5m ago)   3h17m
local-path-storage              pod/local-path-provisioner-58cc7856b6-gbffv                 1/1     Running     0              3h17m
monitoring                      pod/grafana-deployment-c7777965c-7r47z                      1/1     Running     0              162m
opentelemetry-operator-system   pod/otel-operator-opentelemetry-operator-7f55bcdbff-d4t5z   2/2     Running     0              57m

NAMESPACE                       NAME                                           TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                               AGE
default                         service/kubernetes                             ClusterIP   10.96.0.1       <none>        443/TCP                               3h17m
ingress-nginx                   service/ingress-nginx-controller               NodePort    10.96.185.100   <none>        80:30932/TCP,443:31094/TCP            3h16m
ingress-nginx                   service/ingress-nginx-controller-admission     ClusterIP   10.96.33.221    <none>        443/TCP                               3h16m
kube-system                     service/ksm-kube-state-metrics                 ClusterIP   10.96.206.230   <none>        8080/TCP                              3m22s
kube-system                     service/kube-dns                               ClusterIP   10.96.0.10      <none>        53/UDP,53/TCP,9153/TCP                3h17m
monitoring                      service/grafana-service                        ClusterIP   10.96.148.62    <none>        3000/TCP,4318/TCP,4317/TCP,9090/TCP   162m
opentelemetry-operator-system   service/otel-operator-opentelemetry-operator   ClusterIP   10.96.241.253   <none>        8443/TCP,8080/TCP                     57m

NAMESPACE     NAME                        DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
kube-system   daemonset.apps/kindnet      1         1         1       1            1           kubernetes.io/os=linux   3h17m
kube-system   daemonset.apps/kube-proxy   1         1         1       1            1           kubernetes.io/os=linux   3h17m

NAMESPACE                       NAME                                                   READY   UP-TO-DATE   AVAILABLE   AGE
ingress-nginx                   deployment.apps/ingress-nginx-controller               1/1     1            1           3h16m
kube-system                     deployment.apps/coredns                                2/2     2            2           3h17m
kube-system                     deployment.apps/ksm-kube-state-metrics                 1/1     1            1           3m22s
local-path-storage              deployment.apps/local-path-provisioner                 1/1     1            1           3h17m
monitoring                      deployment.apps/grafana-deployment                     1/1     1            1           162m
opentelemetry-operator-system   deployment.apps/otel-operator-opentelemetry-operator   1/1     1            1           57m

NAMESPACE                       NAME                                                              DESIRED   CURRENT   READY   AGE
ingress-nginx                   replicaset.apps/ingress-nginx-controller-77cdd96884               1         1         1       3h16m
kube-system                     replicaset.apps/coredns-668d6bf9bc                                2         2         2       3h17m
kube-system                     replicaset.apps/ksm-kube-state-metrics-8c88554fd                  1         1         1       3m22s
local-path-storage              replicaset.apps/local-path-provisioner-58cc7856b6                 1         1         1       3h17m
monitoring                      replicaset.apps/grafana-deployment-c7777965c                      1         1         1       162m
opentelemetry-operator-system   replicaset.apps/otel-operator-opentelemetry-operator-7f55bcdbff   1         1         1       57m

NAMESPACE       NAME                                       STATUS     COMPLETIONS   DURATION   AGE
ingress-nginx   job.batch/ingress-nginx-admission-create   Complete   1/1           48s        3h16m
ingress-nginx   job.batch/ingress-nginx-admission-patch    Complete   1/1           65s        3h16m
```

We got all the K8s instrumentation installed, now we need to set up Open telemetry to receiver and send traces/logs/metrics to grafana lgtm stack.

### 4️⃣ Configuring Otel to receiver and send data to grafana lgtm stack.

Two ways to change/overwriting the otel default config inside of grafana/otel-lgtm image, you could do:

Via Docker file
```docker
COPY otel/otelcol-config-postgres.yaml /otel-lgtm/otelcol-config.yaml
``` 
Or via Configmap/service account
[config-map.yaml](lgtm/config/otel/otel-config-map.yaml) and [rbac-otel.yaml](lgtm/config/otel/rbac-otel.yaml)

Inside of [k8s.yaml](lgtm/k8s.yaml) uncommnet this parts:
```
# serviceAccountName: lgtm-sa
```

and this:
```
#          volumeMounts:
#            - name: otelcol-config
#              mountPath: /otel-lgtm/otelcol-config.yaml
#              subPath: otelcol-config.yaml
#            - name: varlogpods
#              mountPath: /var/log/pods
#              readOnly: true
#            - name: varlibdockercontainers
#              mountPath: /var/lib/docker/containers
#              readOnly: true
#      # In your Pod/Deployment/DaemonSet spec
#      volumes:
#        - name: varlogpods
#          hostPath:
#            path: /var/log/pods
#        - name: varlibdockercontainers # Sometimes needed for symlinks
#          hostPath:
#            path: /var/lib/docker/containers
#        - name: otelcol-config
#          configMap:
#            name: otelcol-config
```

What does it do?

- Create a service account, cluster rules in order to access k8s using rbac
- Overwriting the otel config to receive and send data to grafana lgtm (Loki, Tempo and Prometheus)

Let's applying the changes and restart the grafana deployment.
```
cd lgtm
# Apply config-map config
kubectl apply -f config-map.yaml

# Apply rbac allowing otel 
kubectl apply -f rbac-otel.yaml

# Change the grafana k8s config
kubectl apply -f k8s.yaml

# restart the grafana deplyoment
kubectl rollout restart -n monitoring deployment grafana-deployment

# After while, verify it
kubectl get all,configmap -n monitoring
NAME                                      READY   STATUS    RESTARTS   AGE
pod/grafana-deployment-6f47f4d485-f57vg   1/1     Running   0          3m29s

NAME                      TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)                               AGE
service/grafana-service   ClusterIP   10.96.148.62   <none>        3000/TCP,4318/TCP,4317/TCP,9090/TCP   3h35m

NAME                                 READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/grafana-deployment   1/1     1            1           3h35m

NAME                                            DESIRED   CURRENT   READY   AGE
replicaset.apps/grafana-deployment-6f47f4d485   1         1         1       3m30s
replicaset.apps/grafana-deployment-85d6f74fbf   0         0         0       29m
replicaset.apps/grafana-deployment-865d74c68b   0         0         0       3m34s
replicaset.apps/grafana-deployment-c7777965c    0         0         0       3h35m

NAME                         DATA   AGE
configmap/kube-root-ca.crt   1      3h35m
configmap/otelcol-config     1      31m
```

Go to http://localhost/grafana/drilldown -> click logs, you see logs from k8s, sooner we deploy any app will be displayed as well.

![k8s-logs.png](k8s-logs.png)

Go to http://localhost/grafana/drilldown -> click metrics, you'll see metrics starting with k8s_*, kube_*, container_* etc.

![k8s-metrics.png](k8s-metrics.png)

Here a list of metrics you can play around and create your board [k8s-metrics.txt](lgtm/boards/k8s/k8s-metrics.txt)

Here is Cluster overview dashboard
![k8s-cluster-overview.png](k8s-cluster-overview.png)

Now it's time to instrument some apps

### 4️⃣ Instrumenting FastAPI app using Otel modules
we are going to use some of these modules below to instrument FastAPI apps, use it accordingly.
```
# Must have
opentelemetry-distro                            # Provides the OTEL SDK + API.
opentelemetry-exporter-otlp                     # Allows exporting through OTLP (HTTP/gRPC).
opentelemetry-instrumentation-logging           # This one injects trace_id and span_id into your logs automatically.

# Option is you are using one of these modules
opentelemetry-instrumentation-fastapi            # Auto-instruments FastAPI routes.
opentelemetry-instrumentation-asyncio            # Helps propagate OTEL context between asyncio tasks — recommended but not required.
opentelemetry-instrumentation-aiohttp-client     # Auto-instruments aiohttp client calls.
opentelemetry-instrumentation-requests           # Auto-instruments the requests library.
opentelemetry-instrumentation-httpx              # Auto-instruments HTTPX (sync/async).
opentelemetry-instrumentation-grpc               # Auto-instruments gRPC client/server.
opentelemetry-instrumentation-aiokafka           # Auto-instruments aiokafka producer/consumer automatically.
opentelemetry-instrumentation-sqlalchemy         # Auto-instruments SQL queries executed by SQLAlchemy.
opentelemetry-instrumentation-asyncpg            # Auto-instruments raw asyncpg queries.
opentelemetry-instrumentation-psycopg2           # Auto-instruments PostgreSQL calls using psycopg2 (sync).
opentelemetry-instrumentation-redis              # Auto-instruments Redis client operations.
```

If you check [Dockerfile](fastapi-msc-test/Dockerfile) you will some ENV set up the auto-instrument.

```docker
# Core environment variables for OpenTelemetry
ENV OTEL_SERVICE_NAME=fastapi-msc-test \
    OTEL_LOG_LEVEL=warning \
    OTEL_PYTHON_INSTRUMENTATION_FASTAPI_ENABLED=true \
    OTEL_PYTHON_INSTRUMENTATION_HTTP_ENABLED=true \
    OTEL_METRIC_EXPORT_INTERVAL=5000 \
    OTEL_METRIC_EXPORT_TIMEOUT=5000 \
    OTEL_EXPORTER_OTLP_COMPRESSION=gzip \
    OTEL_EXPORTER_OTLP_PROTOCOL=grpc \
    OTEL_EXPORTER_OTLP_INSECURE=true \
    OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://grafana-service.monitoring.svc.cluster.local:4317 \
    OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://grafana-service.monitoring.svc.cluster.local:4317 \
    OTEL_PYTHON_FASTAPI_EXCLUDED_URLS="health,metrics,healthz" \
    OTEL_RESOURCE_ATTRIBUTES="service.version=1.0,deployment.environment=development,team=my-team" \
    TZ=America/Sao_Paulo
```

** we are not sending logs, because we already have it via k8s instrumentation.

There is a plenty of option for the OTEL core, and for specifics stacks.
<br><br>
[OTEL - Core](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables)<br> 
[OTEL - Python](https://opentelemetry.io/docs/zero-code/python/configuration)<br>
[OTEL - Java](https://opentelemetry.io/docs/zero-code/java/)<br>
[OTEL - Js](https://opentelemetry.io/docs/zero-code/js/)

### 5️⃣  Deploy Sample Applications "[fastapi-msc-test](fastapi-msc-test)"

```
# Let's build the docker image and deploy it into k8s
cd fastapi-msc-test
docker build --no-cache  --tag fastapi-msc-test:1.0 .

#Load docker image into Kind cluster
kind load docker-image fastapi-msc-test:1.0
 
# For all application we need create a k8s namespace, otherwise it's use default which is not good, just run it once.
kubectl create namespace applications

# Apply k8s.yaml that has deployment/service/ingress route
kubectl apply -f k8s.yaml

# check if pod is running
kubectl get -n applications pods 
NAME                                          READY   STATUS        RESTARTS   AGE
fastapi-msc-test-deployment-f5747c55f-btppl   1/1     Running       0          30s

# Extras command in case you want check the logs or restart the deployment
kubectl logs -n applications deployments/fastapi-msc-test-deployment
kubectl rollout restart -n applications deployment fastapi-msc-test-deployment

# test using curl 
curl http://localhost/fastapi/hello?name=test
{"hello":"test"} 

curl --location 'http://localhost/fastapi/rolldice?player=test'
{"result": "5"}

curl --location 'http://localhost/fastapi/error?code=422'
{
"error_type": "Directly Passed Status Code",
"requested_status_code": 422
}
```
Here is logs via k8s instrumentation of FastAPI app test.

![fastapi-test-logs.png](fastapi-test-logs.png)


OK, we got k8s running, first app running, grafana, working through ingress controller, instrumentation, so far so good. ✅

### 6️⃣ Let's create a dashboard for a FastAPI app.

The main metrics to monitor are:
- Total request per status code
- Total request
- RPS (sum)
- Active Requests
- RPS by Route
- Request Latency (p50, p95, p99)
- RPS by Route/code
- Request Breakdown by Route and Status
- Traces
- Calls Correlation

Playing around as your needs.

📊 FastAPI Board

![fastapi-k8s-board.png](fastapi-k8s-board.png)

This board can be found here [fastapi-k8s-board.json](lgtm/boards/fastapi/fastapi-k8s-board.json)


## 🎯 Key Observability Features Demonstrated

### 🔹 **Automatic Tracing** across microservices

* Kafka → FastAPI
* FastAPI → PostgreSQL
* FastAPI → other services
* Spring Boot → Kafka → DB

### 🔹 **Logs correlated with Traces** using Loki

### 🔹 **Metrics for all workloads** (HTTP, JVM, DB, Kafka, Python, etc.)

### 🔹 **Service Graphs generated by Tempo + Grafana**

### 🔹 **Dashboards using Prometheus metrics**

---

## 🧪 Load Testing Examples

You can use `hey` or `k6` to generate traffic.

Example with `hey`:

```
hey -n 20000 -c 100 \
  -m POST \
  -H "Content-Type: application/json" \
  -d '{"key":"user1","value":"hello world"}' \
  http://localhost/api/produce
```

---

## 🛠 Troubleshooting

### Not seeing traces?

* Check OTEL Collector endpoint in your apps
* Verify kube-dns is working
* Ensure OTLP exporters are configured

### Not seeing logs?

* Verify Loki is running
* Ensure OTEL logger provider is enabled

### Not seeing metrics?

* Confirm Prometheus scraping config
* Ensure OTEL metrics exporter is active

---

## ❤️ Contributions

Feel free to open PRs for:

* new sample apps
* new dashboards
* new observability experiments

---

Enjoy the setup and happy observability! 🎉 🚀
