from opentelemetry import metrics

def setup_metrics(app, service_name: str):
    meter = metrics.get_meter(service_name)
    request_counter = meter.create_counter(
        "app_requests_total",
        description="Total requests"
    )

    @app.middleware("http")
    async def count_requests(request, call_next):
        response = await call_next(request)
        request_counter.add(1, {"method": request.method, "status": response.status_code})
        return response

