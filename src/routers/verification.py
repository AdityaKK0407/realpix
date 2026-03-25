import logging
import os
from typing import Union

import httpx
import redis.asyncio as redis
from fastapi import APIRouter, Depends, Header, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.dependencies import (
    get_activate_token_sha,
    get_create_sha,
    get_ip_rate_limiter_sha,
    get_redis,
)
from src.redis_client.ip_rate_limiter import verify_ip_rate_limiter
from src.redis_client.rate_limiter import (
    activate_rate_limiter_token,
    create_rate_limiter_token,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/verify", tags=["Verification"])


class TurnstileResult(BaseModel):
    success: bool


@router.post("/captcha", response_model=None)
async def verify_captcha(
    payload: dict[str, str],
    x_client_ip: str | None = Header(None),
    x_ratelimit_token: str | None = Header(None),
    redis_client: redis.Redis = Depends(get_redis),
    create_sha: str = Depends(get_create_sha),
    ip_rate_limiter_sha: str = Depends(get_ip_rate_limiter_sha),
    activate_token_sha: str = Depends(get_activate_token_sha),
) -> dict[str, str] | JSONResponse:
    cloudflare_token = payload.get("token", None)

    if not cloudflare_token:
        logger.warning("Missing cloudflare turnstile token in request body")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"status": "error", "detail": "Missing CAPTCHA token"},
        )

    if not x_client_ip:
        logger.error("Missing Client IP in header")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": "error",
                "detail": "Missing Client IP",
            },
        )

    if not await verify_ip_rate_limiter(
        redis_client, ip_rate_limiter_sha, x_client_ip, "verification"
    ):
        logger.warning("Client IP token exceeded rate limit")
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={
                "status": "error",
                "detail": "Rate limit exceeded",
            },
        )

    url = os.getenv("CLOUDFLARE_URL")
    secret_key = os.getenv("CLOUDFLARE_SECRET_KEY")

    if not url or not secret_key:
        logger.error(
            "Failed to read cloudflare url and cloudflare secret key env variables"
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "error", "detail": "Unexpected server error"},
        )

    try:
        success = await verify_turnstile(url, secret_key, cloudflare_token, x_client_ip)
    except Exception as e:
        logger.error(f"Failed to verify turnstile with cloudflare server: {e}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content={
                "status": "error",
                "detail": "Unable to verify request at this time. Please try again later",
            },
        )

    if not success:
        logger.warning("Client provided invalid turnstile token in body")
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"status": "error", "detail": "Invalid CAPTCHA token"},
        )

    try:
        if x_ratelimit_token and await activate_rate_limiter_token(
            redis_client, activate_token_sha, x_ratelimit_token
        ):
            return {"status": "success", "user_token": x_ratelimit_token}

        uuid_token = await create_rate_limiter_token(redis_client, create_sha)
        return {"status": "success", "user_token": uuid_token}

    except Exception as e:
        logger.error(f"Redis service failed to add rate limiter token: {e}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "error",
                "detail": "Service temporarily unavailable",
            },
        )


async def verify_turnstile(
    url: str, secret_key: str, cloudflare_token: str, host: str
) -> bool:
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url,
            data=dict(secret=secret_key, response=cloudflare_token, remoteip=host),
        )
        result = TurnstileResult.model_validate(resp.json())

    return result.success
