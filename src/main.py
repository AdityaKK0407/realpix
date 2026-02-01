import os
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from src.initializer import create_redis_client, load_lua_script
from src.routers.verification import router as verification_router
from src.routers.model import router as model_router


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    load_dotenv()

    host = os.getenv("REDIS_HOST")
    port = int(os.getenv("REDIS_PORT"))
    fastapi_app.state.redis_client = create_redis_client(host, port)
    fastapi_app.state.create_sha = load_lua_script(app.state.redis_client, "src/redis_scripts/create.lua")
    fastapi_app.state.verify_sha = load_lua_script(app.state.redis_client, "src/redis_scripts/verify.lua")
    yield
    fastapi_app.state.redis_client.close()


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
