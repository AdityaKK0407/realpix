import os
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from dotenv import load_dotenv
from fastapi import FastAPI, Response, status

from src.helpers import create_redis_client, load_lua_script, setup_logger
from src.routers.model import router as model_router
from src.routers.verification import router as verification_router

load_dotenv()
PRODUCTION = os.getenv("SERVER") == "production"

setup_logger()

@asynccontextmanager
async def lifespan(fastapi_app: FastAPI) -> AsyncGenerator[None, Any]:

    host = os.getenv("REDIS_HOST")
    port = os.getenv("REDIS_PORT")

    if not host or not port:
        raise RuntimeError("Failed to get env variables")
    try:
        fastapi_app.state.redis_client = create_redis_client(host, int(port))
        fastapi_app.state.create_sha = await load_lua_script(
            fastapi_app.state.redis_client, "src/redis_scripts/create.lua"
        )
        fastapi_app.state.verify_sha = await load_lua_script(
            fastapi_app.state.redis_client, "src/redis_scripts/verify.lua"
        )
        fastapi_app.state.activate_token_sha = await load_lua_script(
            fastapi_app.state.redis_client, "src/redis_scripts/activate_token.lua"
        )
        fastapi_app.state.ip_rate_limiter_sha = await load_lua_script(
            fastapi_app.state.redis_client, "src/redis_scripts/ip_rate_limiter.lua"
        )
    except Exception as e:
        raise RuntimeError(f"Failed to start server: {e}")
    try:
        yield
    finally:
        await fastapi_app.state.redis_client.close()


app = FastAPI(
    lifespan=lifespan,
    docs_url=None if PRODUCTION else "/docs",
    redoc_url=None if PRODUCTION else "/redoc",
    openapi_url=None if PRODUCTION else "/openapi.json",
)
app.include_router(model_router)
app.include_router(verification_router)


@app.head("/")
async def health_check() -> Response:
    return Response(status_code=status.HTTP_200_OK)