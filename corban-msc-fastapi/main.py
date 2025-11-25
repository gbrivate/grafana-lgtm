import asyncio

from fastapi import FastAPI, Request, Query
from random import randint


import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# --- Routes ---
@app.get("/slow")
async def slow():
    await asyncio.sleep(5)  # Keeps the request "active" for 5s
    return {"message": "done"}

@app.get("/rolldice")
async def roll_dice(player: str | None = Query(default=None)):
    result = str(randint(1, 6))
    if player:
        logger.info("%s is rolling the dice: %s", player, result)
    else:
        logger.warning("Anonymous player is rolling the dice: %s", result)
    return {"result": result}

@app.get("/hello")
async def hello(name: str):
    if name == "corban":
        logger.error("Not ok: %s", name )
        return {"Not hello": name}
    logger.info("Hello: %s", name)
    return {"hello": name}

@app.get("/error")
async def get_custom_error(code: int):
    logger.error(f"Generating custom response with Status Code: {code}")
    return JSONResponse(
        status_code=code,
        content={
            "error_type": "Directly Passed Status Code",
            "requested_status_code": code
        },
    )
