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

All services are accessible through a single ingress (e.g. `http://localhost:{{port}}/<service>`).

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

## ▶️ How to start

> Instructions depend on your cluster setup and repo structure.

Example workflow:

```bash
# Create cluster\kind create cluster --config kind-config.yaml

# Deploy LGTM stack
kubectl apply -f lgtm/

# Deploy sample apps
kubectl apply -f apps/
```

---

## 📝 Purpose

This repository exists to provide a **complete, ready‑to‑use local observability lab**:

* Perfect for learning OTEL
* Testing distributed tracing
* Building dashboards
* Understanding Kubernetes observability patterns
* Experimenting with multiple languages and workloads


---

Enjoy the setup and happy observability! 🎉
