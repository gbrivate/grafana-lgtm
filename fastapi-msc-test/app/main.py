import asyncio
import httpx
import base64

from fastapi import FastAPI, Query, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from random import randint

from observability.config import setup_logging
from observability.metrics import setup_metrics

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization


# Initialize logging before the app starts
logger = setup_logging()

app = FastAPI()

# Attach the metrics middleware
setup_metrics(app, "fastapi-msc-test")

# Carregar sua chave privada (exemplo simplificado)
with open("private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None
    )

# --- Carregar a chave pública ---
with open("public_key.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read()
    )

@app.post("/sign-document")
async def sign_document(request: Request):
    # Lê o corpo da requisição como texto
    body_bytes = await request.body()

    # 1. Gera o Hash e Assina em um único passo pela biblioteca
    signature = private_key.sign(
        body_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # Retorna a assinatura em Base64 para ser fácil de transportar
    return {
        "status": "signed",
        "signature": base64.b64encode(signature).decode('utf-8')
    }

# --- Carregar a chave pública ---
with open("public_key.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read()
    )

@app.post("/verify-document")
async def verify_document(request: Request):
    # O ideal é que o cliente envie o dado original e a assinatura.
    # Vamos supor que a assinatura venha num Header ou Query Param
    # e o corpo seja o dado original.

    signature_base64 = request.headers.get("X-Signature")
    if not signature_base64:
        raise HTTPException(status_code=400, detail="Assinatura não encontrada no header X-Signature")

    try:
        # 1. Recupera o dado original (bytes)
        original_data = await request.body()

        # 2. Converte a assinatura de volta de Base64 para Bytes
        signature_bytes = base64.b64decode(signature_base64)

        # 3. Verificação
        # O método .verify() não retorna nada se estiver correto.
        # Se falhar, ele lança uma exceção 'InvalidSignature'.
        public_key.verify(
            signature_bytes,
            original_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        return {
            "status": "valid",
            "message": "A assinatura é autêntica."
            }

    except Exception:
        # Se entrar aqui, a assinatura é falsa ou o dado foi alterado
        raise HTTPException(status_code=401, detail="Assinatura inválida ou dado corrompido")

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
    url = "http://java-msc-test-service.applications.svc.cluster.local:8080/api/loop?id="+str(loop)

    async with httpx.AsyncClient() as client:
        response = await client.get(url,  timeout=httpx.Timeout(30.0))

    logger.info("External service called", extra={"url": url, "status": response.status_code})

    return {
        "called_url": url,
        "remote_status": response.status_code,
        "remote_response": response.text,
    }