from fastapi import APIRouter, Request, Depends, HTTPException, status

import redis
import os
import httpx

from src.redis_client import create_rate_limiter_token
from src.dependencies import get_redis, get_create_sha

router = APIRouter(prefix="/verify", tags=["Verification"])


@router.post("/captcha")
async def verify_captcha(payload: dict[str, str], request: Request, redis_client: redis.Redis = Depends(get_redis),
                         create_sha: str = Depends(get_create_sha)) -> dict[str, str]:
    cloudflare_token = payload["token"]

    if not cloudflare_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing CloudFlare Turnstile Token"
        )

    url = os.getenv("CLOUDFLARE_URL")
    secret_key = os.getenv("CLOUDFLARE_SECRET_KEY")

    async with httpx.AsyncClient() as client:
        resp = await client.post(url, data={
            "secret": secret_key,
            "response": cloudflare_token,
            "remoteip": request.client.host
        })
        result: dict = resp.json()

        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid captcha"
            )

    server_token = request.headers.get("X-RateLimit-Token")

    if server_token:
        return {"user_token": server_token}

    try:
        uuid_token = create_rate_limiter_token(redis_client, create_sha)
        return {"user_token": uuid_token}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Redis failed"
        )
