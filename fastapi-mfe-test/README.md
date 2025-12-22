## Docker
docker build --tag fastapi-mfe-test:latest .
kind load docker-image fastapi-mfe-test 
kubectl rollout restart deployment fastapi-mfe-test-deployment -n applications
kubectl port-forward svc/fastapi-mfe-test-service 8002:8002 -n applications


docker run -p 8002:8002 fastapi-mfe-test:latest

kubectl logs -n applications deployments/fastapi-mfe-test-deployment -f




clear
docker image remove fastapi-mfe-test:latest 
kubectl delete -n applications deployments.apps fastapi-mfe-test-deployment
docker build --tag fastapi-mfe-test:latest .
kind load docker-image fastapi-mfe-test
kubectl apply -f k8s.yaml
kubectl logs -n applications deployments/fastapi-mfe-test-deployment -f


docker container stop fastapi
docker container remove fastapi
docker build --no-cache  --tag fastapi-mfe-test:latest .
docker run -p 8001:8001 \
    --name fastapi \
    --network=mynet \
    -t fastapi-mfe-test:latest



kubectl logs deployments/fastapi-mfe-test-deployment -n applications
kubectl logs deployments/fastapi-mfe-test-deployment -n applications | grep grafana


hey -n 1000 -c 1 -q 1 http://localhost:8080/fastapi/rolldice?player=gabriel
hey -n 10 -c 1 -q 1 http://localhost:8080/fastapi/slow



# Bancos e Mensageria (Drivers)
sqlalchemy
aioredis  # ou redis
aiokafka
psycopg2-binary # se usar Postgres

## OpenTelemetry Core
opentelemetry-distro
opentelemetry-exporter-otlp


## OpenTelemetry - Comunicação HTTP e Chamadas de API
# asgi / fastapi: Capturam o início da requisição, rotas e tempo total de resposta no servidor.
# httpx / requests / aiohttp-client: Monitoram chamadas para APIs externas (quem seu serviço chama).
# grpc: Monitora chamadas de alta performance via protocolo gRPC

opentelemetry-instrumentation-requests
opentelemetry-instrumentation-httpx
opentelemetry-instrumentation-aiohttp-client
opentelemetry-instrumentation-grpc

## OpenTelemetry - Infraestrutura e Servidor
# asyncio: Monitora a saúde e latência das tarefas assíncronas do Python.

opentelemetry-instrumentation-asyncio
opentelemetry-instrumentation-asyncpg
opentelemetry-instrumentation-asgi

## OpenTelemetry - Banco de Dados e Cache (Persistência)
# sqlalchemy: Rastreia queries geradas pelo ORM e tempo de execução no banco.
# sycopg2 / asyncpg: Instrumentam o driver do PostgreSQL (síncrono e assíncrono).
# redis: Monitora comandos de cache (GET, SET) e latência do servidor Redis.

opentelemetry-instrumentation-sqlalchemy
opentelemetry-instrumentation-psycopg2
opentelemetry-instrumentation-redis

## OpenTelemetry - Mensageria e Logs
# aiokafka: Conecta traces entre produtores e consumidores de mensagens Kafka (Tracing Distribuído).
# logging: Injeta automaticamente o trace_id em cada linha de log, permitindo cruzar logs com gráficos no Grafana.

opentelemetry-instrumentation-aiokafka
opentelemetry-instrumentation-logging

