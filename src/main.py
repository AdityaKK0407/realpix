import os
import sys
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.redis_client.client import create_redis_client, load_lua_script
from src.routers.model import router as model_router
from src.routers.verification import router as verification_router


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI) -> AsyncGenerator[None, Any]:
    if not load_dotenv():
        print("Failed to load .env")
        sys.exit(1)

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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(model_router)
app.include_router(verification_router)


@app.get("/")
def home() -> dict[str, str]:
    return {"status": "running"}
