from opentelemetry import metrics

meter = metrics.get_meter("corban-msc-fastapi")
request_counter = meter.create_counter(
    "app_requests_total",
    description="Total number of processed requests"
)

@app.middleware("http")
async def count_requests(request, call_next):
    response = await call_next(request)
    request_counter.add(1, {"method": request.method, "status_code": response.status_code})
    return response

# app_requests_total{service_name="corban-msc-fastapi"}