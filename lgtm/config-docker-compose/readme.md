# Start everything
docker compose up -d

# Check services:

Service	URL
Grafana	http://localhost:3000 (admin / admin)
Loki API	http://localhost:3100
Tempo	http://localhost:3200
Mimir	http://localhost:9009
OTLP receiver	http://localhost:4318

# Optional: Send test data
Test logs
curl -X POST http://localhost:4318/v1/logs -d '{}'

Test traces
curl -X POST http://localhost:4318/v1/traces -d '{}'

Test metrics
curl -X POST http://localhost:4318/v1/metrics -d '{}'

