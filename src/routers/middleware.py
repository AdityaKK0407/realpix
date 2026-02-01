from fastapi import Request, Depends, HTTPException, status

import redis
from redis.exceptions import RedisError

from src.redis_client import verify_rate_limiter_token
from src.dependencies import get_redis, get_verify_sha
from src.redis_client import VerifyTokenResult


async def rate_limiter_middleware(request: Request, redis_client: redis.Redis = Depends(get_redis),
                                  verify_sha: str = Depends(get_verify_sha)):
    token = request.headers.get("X-RateLimit-Token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Missing Rate Limit Token"
        )

    try:
        match verify_rate_limiter_token(redis_client, verify_sha, token):
            case VerifyTokenResult.FAILED:
                ...
            case VerifyTokenResult.INVALID:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Rate Limit Exceeded"
                )
            case VerifyTokenResult.SUCCESS:
                ...
            case VerifyTokenResult.UNREACHABLE:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Server failed"
                )
    except RedisError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Redis failed"
        )
