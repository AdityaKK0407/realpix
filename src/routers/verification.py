import os

import httpx
import redis.asyncio as redis
from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from pydantic import BaseModel

from src.dependencies import get_activate_token_sha, get_create_sha, get_redis
from src.redis_client.rate_limiter import (
    activate_rate_limiter_token,
    create_rate_limiter_token,
)

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
    activate_token_sha: str = Depends(get_activate_token_sha),
) -> dict[str, str]:
    cloudflare_token = payload.get("token", None)

    if not cloudflare_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Missing CAPTCHA token"
        )

    url = os.getenv("CLOUDFLARE_URL")
    secret_key = os.getenv("CLOUDFLARE_SECRET_KEY")

    if not url or not secret_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error",
        )

    user = request.client
    if not user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Client not available",
        )

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                url,
                data=dict(
                    secret=secret_key, response=cloudflare_token, remoteip=user.host
                ),
            )
            result = TurnstileResult.model_validate(resp.json())
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Unable to verify request at this time. Please try again later",
            )

        if not result.success:
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
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service temporarily unavailable",
        )
