import redis
import uuid
from enum import Enum

TOTAL_QUOTA = 100
BUCKET_SIZE = 10
RATE_PER_MIN = 2
RATE_PER_SECOND = RATE_PER_MIN / 60
TTL_SECONDS = 30 * 24 * 60 * 60

class VerifyTokenResult(Enum):
    FAILED = -1
    INVALID = 0
    SUCCESS = 1
    UNREACHABLE = 2

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


def verify_rate_limiter_token(client: redis.Redis, create_script_sha: str, uuid_key: str) -> VerifyTokenResult:
    key = f'rate_limiter:token:{uuid_key}'

    match client.evalsha(
        create_script_sha,
        1,
        key,
        BUCKET_SIZE,
        RATE_PER_SECOND
    ):
        case -1:
            return VerifyTokenResult.FAILED
        case 0:
            return VerifyTokenResult.INVALID
        case 1:
            return VerifyTokenResult.SUCCESS
        case _:
            return VerifyTokenResult.UNREACHABLE