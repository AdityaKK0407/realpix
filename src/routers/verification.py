import os

import httpx
import redis.asyncio as redis
from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
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
from src.helpers import logger

router = APIRouter(prefix="/verify", tags=["Verification"])


class TurnstileResult(BaseModel):
    success: bool


@router.post("/captcha")
async def verify_captcha(
    payload: dict[str, str],
    request: Request,
    x_ratelimit_token: str | None = Header(None),
    redis_client: redis.Redis = Depends(get_redis),
    create_sha: str = Depends(get_create_sha),
    ip_rate_limiter_sha: str = Depends(get_ip_rate_limiter_sha),
    activate_token_sha: str = Depends(get_activate_token_sha),
) -> dict[str, str]:
    cloudflare_token = payload.get("token", None)

    if not cloudflare_token:
        logger.warning("Missing cloudflare turnstile token in request body")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Missing CAPTCHA token"
        )

    user = request.client
    if not user:
        logger.warning("Client IP missing in request")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Client not available",
        )

    if not await verify_ip_rate_limiter(
        redis_client, ip_rate_limiter_sha, user.host, "verification"
    ):
        logger.warning("Client IP token exceeded rate limit")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded",
        )

    url = os.getenv("CLOUDFLARE_URL")
    secret_key = os.getenv("CLOUDFLARE_SECRET_KEY")

    if not url or not secret_key:
        logger.error("Failed to read cloudflare url and cloudflare secret key env variables")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error",
        )

    try:
        success = await verify_turnstile(url, secret_key, cloudflare_token, user.host)
    except Exception:
        logger.error("Failed to verify turnstile with cloudflare server")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to verify request at this time. Please try again later",
        )

    if not success:
        logger.warning("Client provided invalid turnstile token in body")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid CAPTCHA token"
        )

    try:
        if x_ratelimit_token and await activate_rate_limiter_token(
            redis_client, activate_token_sha, x_ratelimit_token
        ):
            return {"user_token": x_ratelimit_token}

        uuid_token = await create_rate_limiter_token(redis_client, create_sha)
        return {"user_token": uuid_token}

    except Exception:
        logger.error("Redis service failed to add rate limiter token")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service temporarily unavailable",
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
