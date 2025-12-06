#!/usr/bin/env bash

watch -c -t -n 1 "clear; kubectl get hpa corban-java-hpa -o jsonpath='📊 App: {.metadata.name}
-----------------------------------------------------
🧠 CPU: {.status.currentMetrics[?(@.resource.name==\"cpu\")].resource.current.averageUtilization}%/{.spec.metrics[?(@.resource.name==\"cpu\")].resource.target.averageUtilization}%{\"\n\"}💾 MEM: {.status.currentMetrics[?(@.resource.name==\"memory\")].resource.current.averageUtilization}%/{.spec.metrics[?(@.resource.name==\"memory\")].resource.target.averageUtilization}%{\"\n\"} ⚡ RPS: {.status.currentMetrics[?(@.object.metric.name==\"http_requests_per_second_java\")].object.current.value}/{.spec.metrics[?(@.object.metric.name==\"http_requests_per_second_java\")].object.target.value}{\"\n\"}⏱️ LAT: {.status.currentMetrics[?(@.object.metric.name==\"http_request_duration_seconds_p95\")].object.current.value}/{.spec.metrics[?(@.object.metric.name==\"http_request_duration_seconds_p95\")].object.target.value}{\"\n\"}🧩 REPLICAS: current={.status.currentReplicas}, desired={.status.desiredReplicas}, min={.spec.minReplicas}, max={.spec.maxReplicas}{\"\n\"}'"




