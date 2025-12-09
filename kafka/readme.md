# Kafka

docker build --no-cache -t kafka-otel:latest .
kind load docker-image kafka-otel:latest
kubectl rollout restart deployment kafka-deployment -n applications
kubectl port-forward svc/kafka-service 7071:7071 -n applications
kubectl get pods  -n applications -w
kubectl logs  deployments/kafka-deployment -n applications


docker build --no-cache -t kafka-otel:latest .
kind load docker-image kafka-otel:latest
kubectl apply -f k8s.yaml

/jmx/rules/kafka-broker.yaml


## Best recommended architecture for Kafka

Kafka JVM
├── jmx_prometheus_javaagent.jar  →  FULL Kafka metrics
└── opentelemetry-javaagent.jar   →  Traces + logs (+ minimal metrics)

Prometheus (inside grafana/otel-lgtm)
scrapes → /metrics (jmx agent)
OTEL Collector (built-in)
receives → traces/logs from OTEL agent
Grafana → visualization

This is textbook production architecture.

clear
docker container stop kafka
docker container remove kafka
docker build --no-cache  --tag kafka:1.0 .
docker run -p 8003:8003 \
    --name kafka \
    --network=mynet \
    -t kafka:1.0

## kafka config files path
/opt/kafka/config

## quota
docker exec -e JAVA_TOOL_OPTIONS='-Dotel.javaagent.enabled=false' -e KAFKA_OPTS='' kafka /opt/kafka/bin/kafka-configs.sh \
--bootstrap-server localhost:9092 \
--alter --add-config 'producer_byte_rate=100,consumer_byte_rate=100' \
--entity-type clients --entity-default

## list metrics inside docker container
docker exec -u 0 kafka sh -c "\
    wget -qO /tmp/jmxterm.jar https://repo1.maven.org/maven2/org/cyclopsgroup/jmxterm/1.0.4/jmxterm-1.0.4-uber.jar && \
    echo 'beans' | java -cp /tmp/jmxterm.jar org.cyclopsgroup.jmxterm.boot.CliMain -l localhost:9101 -n"
 
## logs throttle 
docker exec -e KAFKA_OPTS='' kafka /opt/kafka/bin/kafka-configs.sh --bootstrap-server localhost:9092 --alter --add-config 'producer_byte_rate=1000,consumer_byte_rate=1000' --entity-type clients --entity-default

docker exec kafka tail -f /opt/kafka/logs/server.log | grep -i throttle  