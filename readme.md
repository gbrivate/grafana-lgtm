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
Building and deployment into k8s

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
Open browser at http://localhost/grafana (admim/admin) then you should see that:

![Grafana home page](grafana.png)

### 4️⃣ Instrumenting FastAPI app using Otel modules
we are using some of these modules below to instrument FastAPI apps, use it accordingly.
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
    OTEL_RESOURCE_ATTRIBUTES="service.version=1.0,deployment.environment=development,team=my-team" \
    OTEL_EXPORTER_OTLP_INSECURE=true \
    OTEL_EXPORTER_OTLP_ENDPOINT=http://grafana-service.monitoring.svc.cluster.local:4317 \
    OTEL_PYTHON_LOG_CORRELATION=true \
    OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true \
    OTEL_METRICS_EXPORT_INTERVAL=5000 \
    TZ=America/Sao_Paulo
```

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

OK, we got k8s running, first app running, grafana, working through ingress controller, so far so good. ✅

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

This board can be found here [fastapi-board.json](lgtm/boards/fastapi-board.json)

![fastapi-msc-test-grafana.png](fastapi-msc-test-grafana.png)

📈 There Two-level visibility:

- Application observability → what happens within your code (business logic, requests, errors).
- Platform observability → what happens around your code (Kubernetes, network, resources, infrastructure).

You don't need to choose between instrumenting Kubernetes or an application;
ideally, you should combine both, each with a specific purpose.

📜 Logs via Loki (Application observability, not stdout or stderr logs yet) 


![fastapi-msc-test-logs-grafana.png](fastapi-msc-test-logs-grafana.png)

🎯 Noticed we have a dashboard only with a service name filter, no k8s filters yet, in order to do it, we do need to instrument k8s as well.

### 7️⃣ Instrumenting K8s

One of the best way to instrument Kubernetes (K8s) using OpenTelemetry (Otel) for collecting logs, traces, and metrics is by leveraging the OpenTelemetry Operator combined with the OpenTelemetry Collector.

This approach:
- Centralizes configuration
- Automates collection
- Separates the concerns of data collection from application code, which is ideal for a dynamic container environment like Kubernetes.

1 - Install cert-manager (Often Required)
The OpenTelemetry Operator uses Admission Webhooks for its auto-instrumentation feature (injecting sidecars), which requires TLS certificates. The most common tool for managing these is cert-manager.
```
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.2/cert-manager.yaml
```

2 - Install the OpenTelemetry Operator
```
kubectl apply -f https://github.com/open-telemetry/opentelemetry-operator/releases/latest/download/opentelemetry-operator.yaml
```
8️⃣
9️⃣


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
