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

* Docker
* KinD
* kubectl

---

## 📝 Purpose

This repository exists to provide a **complete, ready‑to‑use local observability lab**:

* Perfect for learning OTEL
* Testing distributed tracing
* Building dashboards
* Understanding Kubernetes observability patterns
* Experimenting with multiple languages and workloads

---

## 📄 License

MIT or your preferred license.

---

## 🧭 Architecture Diagram

Below is a conceptual overview of the observability stack in this repository:

                                User / Browser (http://localhost/...)
                                                |
                                                |
    +-------------------------------------------|-----------------------------------+
    |  KUBERNETES CLUSTER (KinD)                v                                   |
    |                                 +---------------------+                       |
    |                                 |  Ingress Controller |                       |
    |                                 +----------+----------+                       |
    |                                            |                                  |         
    |              ______________________________|_____________                     |
    |            |                                             |                    |
    |            v                                             v                    | 
    |  +---------------------+           +---------------------------------------+  |
    |  |  Ingress Controller |---------->|  LGTM Stack (grafana/otel-lgtm)       |  |
    |  +----------+----------+           |                                       |  |
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

## 🧩 Folder Structure (Recommended)

If your repo already follows another structure, I can adjust this section.

```

repo/
├── apps/
│   ├── fastapi/
│   ├── fastapi-db/
│   ├── springboot/
│   ├── kafka/
│   └── postgres/
│
├── k8s/
│   ├── deployments/
│   ├── services/
│   ├── ingress/
│   └── namespace.yaml
│
├── lgtm/   # Grafana+OTEL stack
│
├── kind-config.yaml
├── README.md
└── docs/
    └── architecture.md
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

We are going to use this docker image 'grafana/otel-lgtm:0.12.0' which has:
```
OpenTelemetry collector => for receiving OpenTelemetry data.
Prometheus              => metrics database.
Tempo                   => trace database.
Loki                    => logs database.
Grafana                 => for visualization.
```

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

# Open brower and test it http://localhost/grafana you should that:
```
![Grafana home page](img.png)

### 4️⃣ Deploy Sample Applications "[fastapi-msc-test](fastapi-msc-test)" 

```
# Let's build the docker image and deploy it into k8s
cd fastapi-msc-test
docker build --no-cache  --tag fastapi-msc-test:latest .

#Load docker image into Kind cluster
kind load docker-image fastapi-msc-test
 
# For all application we need create a k8s namespace, otherwise it's use default which is not good, just run it once.
kubectl create namespace applications

# Apply k8s.yaml that has deployment/service/ingress route
kubectl apply -f k8s.yaml

# check if pod is running
kubectl get -n applications pods 
NAME                                          READY   STATUS        RESTARTS   AGE
fastapi-msc-test-deployment-f5747c55f-btppl   1/1     Running       0          30s

# test using curl "curl http://localhost/fastapi/hello?name=test" you should this response
{"hello":"test"} 
```

### 5️⃣ Instrumenting FastAPI app using Otel modules
The 'fastapi' app is already instrumented, which means, we are using some of these modules below, if you use accordingly.
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

OK, we got k8s running, first app running and working through ingress controller



```
kubectl apply -f lgtm/
```

### 6️⃣

```
kubectl apply -f apps/
```

### 7️⃣ Access Grafana

```
http://localhost/grafana
```

Default credentials (unless modified):

```
user: admin
pass: admin
```
8️⃣
9️⃣
---

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
