import logging

import redis.asyncio as redis
from fastapi import Depends, Header, HTTPException, status

from src.dependencies import get_redis, get_verify_sha
from src.redis_client.rate_limiter import VerifyTokenResult, verify_rate_limiter_token

logger = logging.getLogger(__name__)


async def rate_limiter_middleware(
    x_ratelimit_token: str | None = Header(default=None),
    redis_client: redis.Redis = Depends(get_redis),
    verify_sha: str = Depends(get_verify_sha),
) -> None:
    if not x_ratelimit_token:
        logger.warning("Rate limit token missing in header")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing rate limiter token",
        )

    try:
        match await verify_rate_limiter_token(
            redis_client, verify_sha, x_ratelimit_token
        ):
            case VerifyTokenResult.TOKEN_LIMIT_EXCEEDED:
                logger.warning("Rate limit token expired or invalid")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid rate limiter token",
                )
            case VerifyTokenResult.RATE_LIMITED:
                logger.warning("Rate limiter token exceeded rate limit")
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Rate limit exceeded",
                )
            case VerifyTokenResult.SUCCESS:
                ...
            case VerifyTokenResult.INACTIVE_TOKEN:
                logger.warning("Rate limit token inactive")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Rate limiter token inactive",
                )
            case VerifyTokenResult.UNREACHABLE:
                logger.critical("Redis script executed unreachable code")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Unexpected server error",
                )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Rate limiter token verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service temporarily unavailable",
        )
