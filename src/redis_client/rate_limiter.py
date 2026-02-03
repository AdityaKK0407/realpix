import uuid
from enum import Enum
from typing import Awaitable

import redis.asyncio as redis

TOTAL_QUOTA = 100
BUCKET_SIZE = 10
RATE_PER_MIN = 2
RATE_PER_SECOND = RATE_PER_MIN / 60
TTL_SECONDS = 30 * 24 * 60 * 60


class VerifyTokenResult(Enum):
    TOKEN_LIMIT_EXCEEDED = -1
    RATE_LIMITED = 0
    SUCCESS = 1
    INACTIVE_TOKEN = 2
    UNREACHABLE = 3


async def create_rate_limiter_token(client: redis.Redis, create_script_sha: str) -> str:
    token_id = uuid.uuid4()
    key = f"rate_limiter:token:{token_id}"

    initial_tokens = BUCKET_SIZE

    result = client.evalsha(
        create_script_sha, 1, key, TOTAL_QUOTA, initial_tokens, TTL_SECONDS
    )

    if isinstance(result, Awaitable):
        await result

    return str(token_id)


async def verify_rate_limiter_token(
    client: redis.Redis, verify_script_sha: str, uuid_key: str
) -> VerifyTokenResult:
    key = f"rate_limiter:token:{uuid_key}"

    result = client.evalsha(verify_script_sha, 1, key, BUCKET_SIZE, RATE_PER_SECOND)
    if isinstance(result, Awaitable):
        result = await result

    match int(result):
        case -1:
            return VerifyTokenResult.TOKEN_LIMIT_EXCEEDED
        case 0:
            return VerifyTokenResult.RATE_LIMITED
        case 1:
            return VerifyTokenResult.SUCCESS
        case 2:
            return VerifyTokenResult.INACTIVE_TOKEN
        case _:
            return VerifyTokenResult.UNREACHABLE


async def activate_rate_limiter_token(
    client: redis.Redis, activate_token_sha: str, uuid_key: str
) -> bool:
    key = f"rate_limiter:token:{uuid_key}"

    result = client.evalsha(activate_token_sha, 1, key)
    if isinstance(result, Awaitable):
        result = await result

    return int(result) == 1
