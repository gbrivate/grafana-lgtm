import asyncio
import httpx

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from random import randint

from observability.config import setup_logging
from observability.metrics import setup_metrics


# Initialize logging before the app starts
logger = setup_logging()

app = FastAPI()

# Attach the metrics middleware
setup_metrics(app, "fastapi-msc-test")

@app.get("/slow")
async def slow(timeDelay: int | None = Query(default=5)):
    await asyncio.sleep(timeDelay / 1000)
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
        logger.warning("Not ok", extra={"input_name": name})
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