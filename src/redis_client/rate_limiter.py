import redis
import uuid
from enum import Enum
from typing import cast

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


def create_rate_limiter_token(client: redis.Redis, create_script_sha: str) -> str:
    token_id = uuid.uuid4()
    key = f'rate_limiter:token:{token_id}'

    initial_tokens = BUCKET_SIZE

    client.evalsha(
        create_script_sha,
        1,
        key,
        TOTAL_QUOTA,
        initial_tokens,
        TTL_SECONDS
    )

    return str(token_id)


def verify_rate_limiter_token(client: redis.Redis, verify_script_sha: str, uuid_key: str) -> VerifyTokenResult:
    key = f'rate_limiter:token:{uuid_key}'

    match int(cast(str, client.evalsha(
        verify_script_sha,
        1,
        key,
        BUCKET_SIZE,
        RATE_PER_SECOND
    ))):
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


def activate_rate_limiter_token(client: redis.Redis, activate_token_sha: str, uuid_key: str) -> bool:
    key = f'rate_limiter:token:{uuid_key}'

    result = client.evalsha(
        activate_token_sha,
        1,
        key
    )
    return int(cast(str, result)) == 1
