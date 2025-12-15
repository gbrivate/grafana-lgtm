# 🚀 Kubernetes Observability Dashboard Plan

This document outlines the structure, metrics, and PromQL queries necessary to build a comprehensive, filterable Kubernetes monitoring dashboard in Grafana, utilizing data from `kube-state-metrics` and cAdvisor/Kubelet metrics.

## ✨ Key Features and Filters

The dashboard is designed to be highly dynamic, leveraging Grafana's templating features to allow users to drill down into specific workloads.

### 1. Templating Variables (Filters)

Define these variables in Grafana's **Dashboard Settings > Variables**. Ensure **Multi-value** and **Include All** options are selected for interactive filtering.

| Variable Name | Label | Type | PromQL Query |
| :--- | :--- | :--- | :--- |
| `namespace` | Namespace | Query | `label_values(kube_pod_info, namespace)` |
| `deployment` | Deployment | Query | `label_values(kube_replicaset_owner{namespace=~"$namespace", owner_kind="Deployment"}, owner_name)` |
| `pod` | Pod | Query | `label_values(kube_pod_info{namespace=~"$namespace"}, pod)` |

## 📊 Dashboard Panel Configurations

The panels are organized into logical sections to provide a clear view of the system's state and performance.

### A. Workload Health & Status (Row 1)

These Stat/Gauge panels provide an immediate summary of deployment stability.

| Panel Title | Metric Source | PromQL Query | Visualization | Unit |
| :--- | :--- | :--- | :--- | :--- |
| **Desired Replicas** | `kube_replicaset_spec_replicas` | `sum(kube_replicaset_spec_replicas{namespace=~"$namespace", owner_name=~"$deployment"})` | Stat/Gauge | Count (Short) |
| **Ready Replicas** | `kube_replicaset_status_ready_replicas` | `sum(kube_replicaset_status_ready_replicas{namespace=~"$namespace", owner_name=~"$deployment"})` | Stat/Gauge | Count (Short) |
| **Unready Replicas** | Calculated | `sum(kube_replicaset_spec_replicas{namespace=~"$namespace", owner_name=~"$deployment"}) - sum(kube_replicaset_status_ready_replicas{namespace=~"$namespace", owner_name=~"$deployment"})` | Stat/Gauge | Count (Short) |

---

### B. Resource Utilization (Row 2 - Graph Panels)

These panels track time-series usage for CPU, Memory, and Network I/O. **Note:** Use the `$__rate_interval` variable for `rate()` functions.

#### CPU Usage

| Panel Title | Metric | PromQL Query | Y-Axis Unit | Legend Format |
| :--- | :--- | :--- | :--- | :--- |
| **Pod CPU Usage (Cores)** | `container_cpu_time_seconds_total` | `sum(rate(container_cpu_time_seconds_total{namespace=~"$namespace", pod=~"$pod", container!=""}[$__rate_interval])) by (pod)` | Cores (`short`) | `{{pod}}` |
| **Container CPU Breakdown** | `container_cpu_time_seconds_total` | `sum(rate(container_cpu_time_seconds_total{namespace=~"$namespace", pod=~"$pod", container!=""}[$__rate_interval])) by (pod, container)` | Cores (`short`) | `{{pod}} - {{container}}` |

#### Memory Usage

| Panel Title | Metric | PromQL Query | Y-Axis Unit | Legend Format |
| :--- | :--- | :--- | :--- | :--- |
| **Pod Memory (Working Set)** | `k8s_pod_memory_working_set_bytes` | `sum(k8s_pod_memory_working_set_bytes{namespace=~"$namespace", pod=~"$pod"}) by (pod)` | Bytes (`data(B)`) | `{{pod}}` |
| **Container Memory Breakdown** | `container_memory_usage_bytes` | `sum(container_memory_usage_bytes{namespace=~"$namespace", pod=~"$pod", container!=""}) by (pod, container)` | Bytes (`data(B)`) | `{{pod}} - {{container}}` |
| **Memory Page Fault Ratio** | `container_memory_page_faults_ratio` | `sum(container_memory_page_faults_ratio{namespace=~"$namespace", pod=~"$pod", container!=""}) by (pod, container)` | Percent (0-100) | `{{pod}} - {{container}}` |

#### Network I/O

| Panel Title | Metric | PromQL Query | Y-Axis Unit | Legend Format |
| :--- | :--- | :--- | :--- | :--- |
| **Network RX Rate (Ingress)** | `k8s_pod_network_io_bytes_total` | `sum(rate(k8s_pod_network_io_bytes_total{namespace=~"$namespace", pod=~"$pod", direction="rx"}[$__rate_interval])) by (pod)` | Bytes/sec (`data(B/s)`) | `{{pod}} (Receive)` |
| **Network TX Rate (Egress)** | `k8s_pod_network_io_bytes_total` | `sum(rate(k8s_pod_network_io_bytes_total{namespace=~"$namespace", pod=~"$pod", direction="tx"}[$__rate_interval])) by (pod)` | Bytes/sec (`data(B/s)`) | `{{pod}} (Transmit)` |

---

### C. Storage and Configuration (Row 3)

These panels monitor persistent storage health and configuration objects.

| Panel Title | Metric Source | PromQL Query | Visualization | Unit | Legend Format |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Volume Usage (%)** | `k8s_volume_capacity_bytes`, `k8s_volume_available_bytes` | `((k8s_volume_capacity_bytes{namespace=~"$namespace"} - k8s_volume_available_bytes{namespace=~"$namespace"}) / k8s_volume_capacity_bytes{namespace=~"$namespace"}) * 100` | Graph | Percent (0-100) | `{{persistentvolumeclaim}}` |
| **Volume Inode Ratio** | `k8s_volume_inodes_used_ratio` | `k8s_volume_inodes_used_ratio{namespace=~"$namespace"}` | Graph | Percent (0-100) | `{{persistentvolumeclaim}}` |
| **Total Secrets** | `kube_secret_info` | `count(kube_secret_info{namespace=~"$namespace"})` | Stat | Count (Short) | `N/A` |
| **Services by Type** | `kube_service_info` | `count by (type) (kube_service_info{namespace=~"$namespace", type!=""})` | Table | N/A | `N/A` |
| **Storage Class Count** | `kube_storageclass_info` | `count(kube_storageclass_info)` | Stat | Count (Short) | `N/A` |

---

## 💡 Implementation Tips

* **Filter Inclusion:** Always use regex matching (`=~"$variable"`) in PromQL queries that utilize templating variables.
* **Unit Accuracy:** Set the Y-axis units correctly (Bytes, Bytes/sec, Cores, Percent) for accurate visualization and scaling.
* **Time Range:** For rate metrics, the `$__rate_interval` variable ensures the query step matches the dashboard's time range for consistent results.