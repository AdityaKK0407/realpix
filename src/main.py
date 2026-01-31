import os
from dotenv import load_dotenv
import httpx
from fastapi import FastAPI, UploadFile, HTTPException, Request, status
from src.celery_app import task_queue
from src.tasks import image_task, video_task
from src.redis_client import create_rate_limiter_token, verify_rate_limiter_token, redis_client, create_sha, verify_sha

load_dotenv()

app = FastAPI()

EXCLUDED_PATHS = {
    # FastAPI builtin paths
    "/docs",
    "/redoc",
    "/openapi.json",

    # Server paths
    "/",
    "/verify-captcha"
}


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    if request.url.path not in EXCLUDED_PATHS:
        return await call_next(request)

    token = request.headers.get("X-RateLimit-Token")

    if not token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Missing Rate Limiting token")

    try:
        if not verify_rate_limiter_token(redis_client, verify_sha, token):
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate Limit Exceeded")
    except HTTPException as http_error:
        raise http_error
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Redis failed")

    return await call_next(request)

@app.get("/")
def home() -> dict[str, str]:
    return {"status": "running"}


@app.post("/verify-captcha")
async def verify_captcha(payload: dict[str, str], request: Request) -> dict[str, str]:
    token = payload["token"]

    if not token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing CloudFlare Turnstile Token")

    url = os.getenv("CLOUDFLARE_URL")
    secret_key = os.getenv("CLOUDFLARE_SECRET_KEY")
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, data={"secret": secret_key, "response": token, "remoteip": request.client.host})
        result: dict = resp.json()

        if not result.get("success"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid captcha")

    try:
        uuid_token = create_rate_limiter_token(redis_client, create_sha)
        return {"user_token": uuid_token}
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Redis failed")


@app.post("/start-task-images")
async def start_task_image(images: list[UploadFile]) -> list[dict[str, str]]:
    result: list[dict | None] = [None] * len(images)

    for index, image in enumerate(images):
        content = await image.read()
        task_data = image_task.delay(image.filename, content)
        result[index] = {"task_id": task_data.id}

    return result


@app.post("/start-task-videos")
async def start_task_video(videos: list[UploadFile]) -> list[dict[str, str]]:
    result: list[dict | None] = [None] * len(videos)

    for index, video in enumerate(videos):
        content = await video.read()
        task_data = video_task.delay(video.filename, content)
        result[index] = {"task_id": task_data.id}

    return result


@app.get("/task-status/{task_id}")
async def check_task_status(task_id: str) -> dict:
    task_result = task_queue.AsyncResult(task_id)
    if task_result.state == "SUCCESS":
        return {
            "status": "completed",
            "result": task_result.result
        }
    elif task_result.state == "FAILED":
        return {"status": "failed"}
    else:
        return {"status": "pending"}
