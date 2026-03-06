import sys
import os

from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

import redis.asyncio as redis
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request, status

from src.dependencies import get_ip_rate_limiter_sha, get_redis
from src.redis_client.client import create_redis_client, load_lua_script
from src.redis_client.ip_rate_limiter import verify_ip_rate_limiter
from src.routers.model import router as model_router
from src.routers.verification import router as verification_router

from src.helpers import setup_logger
import logging

setup_logger()

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(fastapi_app: FastAPI) -> AsyncGenerator[None, Any]:
    load_dotenv()

    host = os.getenv("REDIS_HOST")
    port = os.getenv("REDIS_PORT")

    if not host or not port:
        print("Failed to get env variables")
        sys.exit(1)
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
        print(f"Failed to start server: {e}")
        sys.exit(1)

    try:
        yield
    finally:
        await fastapi_app.state.redis_client.close()


app = FastAPI(lifespan=lifespan)
app.include_router(model_router)
app.include_router(verification_router)


@app.head("/")
async def health_check(
    request: Request,
    redis_client: redis.Redis = Depends(get_redis),
    ip_rate_limiter_sha: str = Depends(get_ip_rate_limiter_sha),
):
    user = request.client
    if not user:
        # print("Client IP missing in request", flush=True)
        logger.warning("Client IP missing in request")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Client not available",
        )
    if not await verify_ip_rate_limiter(
        redis_client, ip_rate_limiter_sha, user.host, "health_check"
    ):
        # print("Client IP token exceeded rate limit", flush=True)
        logger.warning("Client IP token exceeded rate limit")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded",
        )
    return {"status": "ok"}
