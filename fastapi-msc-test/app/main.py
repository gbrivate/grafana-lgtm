import asyncio
import httpx
import logging
from random import randint
import json

from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse
# Re-importing pythonjsonlogger, as it's required for JSON formatting
from pythonjsonlogger import jsonlogger

from opentelemetry import metrics
from opentelemetry.trace import get_current_span
from opentelemetry.trace.propagation import set_span_in_context

# --- CUSTOM JSON FORMATTER FOR OTEL CORRELATION ---
class OTelJsonFormatter(jsonlogger.JsonFormatter):
    """
    Custom JSON formatter that injects OpenTelemetry Trace and Span IDs
    into every log record if an active span exists.
    """
    # Arguments: log_data (the final dict), log_record (the immutable record), message_dict (extra fields)
    def add_fields(self, log_data, record, message_dict):
        # 1. Always call the parent method first to populate standard fields
        super(OTelJsonFormatter, self).add_fields(log_data, record, message_dict)

        span = get_current_span()
        span_context = span.get_span_context()

        # 2. Inject Trace and Span IDs into the mutable log_data dictionary
        if span_context.is_valid:
            # FIX: Target the mutable log_data dictionary
            log_data['trace_id'] = format(span_context.trace_id, '032x')
            log_data['span_id'] = format(span_context.span_id, '016x')
        else:
            # FIX: Target the mutable log_data dictionary with placeholders
            log_data['trace_id'] = '00000000000000000000000000000000'
            log_data['span_id'] = '0000000000000000'

# ---------------------------------------------


# ----------------------------------------------------
# Global Logging Configuration (JSON Format)
# ----------------------------------------------------

# 1. Instantiate the JSON formatter and handler
handler = logging.StreamHandler()
# NOTE: Using a list of fields for JSON structure
formatter = OTelJsonFormatter(
    fmt='%(levelname)s %(name)s %(message)s %(asctime)s %(pathname)s %(lineno)d %(funcName)s',
    reserved_attrs=['message', 'levelname', 'name', 'asctime', 'pathname', 'lineno', 'funcName']
)
handler.setFormatter(formatter)

# 2. Configure the root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# Clear existing handlers to avoid duplicates
if root_logger.hasHandlers():
    root_logger.handlers.clear()
root_logger.addHandler(handler)

# 3. Application-specific logger
logger = logging.getLogger(__name__)
if logger.hasHandlers():
    logger.handlers.clear()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# ----------------------------------------------------
# App Initialization
# ----------------------------------------------------
app = FastAPI()

# ----------------------------------------------------
# Metrics (OTEL)
# ----------------------------------------------------
meter = metrics.get_meter("fastapi-msc-test")
request_counter = meter.create_counter(
    "app_requests_total",
    description="Total number of processed requests"
)

@app.middleware("http")
async def count_requests(request, call_next):
    # Log the incoming request with extra fields
    logger.info("Incoming request", extra={"method": request.method, "path": request.url.path})

    response = await call_next(request)
    request_counter.add(1, {"method": request.method, "status_code": response.status_code})
    return response

# ----------------------------------------------------
# Routes
# ----------------------------------------------------

@app.get("/slow")
async def slow():
    await asyncio.sleep(5)
    logger.info("Slow operation complete")
    return {"message": "done"}

@app.get("/rolldice")
async def roll_dice(player: str | None = Query(default=None)):
    result = str(randint(1, 6))
    if player:
        # Use 'extra' dict for key-value fields in JSON logging
        logger.info("Player is rolling the dice", extra={"player": player, "result": result})
    else:
        logger.warning("Anonymous player is rolling the dice", extra={"result": result})
    return {"result": result}

@app.get("/hello")
async def hello(name: str):
    if name == "test":
        logger.warning("Not ok path taken", extra={"input_name": name})
        return {"Not hello": name}

    logger.info("Successfully greeted user", extra={"input_name": name})
    return {"hello": name}

@app.get("/error")
async def get_custom_error(code: int):
    logger.error("Generating custom response with error code", extra={"requested_status_code": code})
    return JSONResponse(
        status_code=code,
        content={
            "error_type": "Directly Passed Status Code",
            "requested_status_code": code
        },
    )

# ----------------------------------------------------
# Call external endpoint
# ----------------------------------------------------
@app.get("/call-loop")
async def call_loop(loop: int | None = Query(default=1)):
    url = "http://java:8080/api/loop?id="+str(loop)

    async with httpx.AsyncClient() as client:
        response = await client.get(url,  timeout=httpx.Timeout(30.0))

    logger.info("External service called", extra={"url": url, "status": response.status_code})

    return {
        "called_url": url,
        "remote_status": response.status_code,
        "remote_response": response.text,
    }