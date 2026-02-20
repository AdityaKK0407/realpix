from typing import Awaitable

import redis.asyncio as redis

IP_BUCKET_SIZE = 10
IP_RATE_PER_MIN = 2
IP_RATE_PER_SECOND = IP_RATE_PER_MIN / 60
IP_TTL = 1800
GLOBAL_BUCKET_SIZE = 100
GLOBAL_RATE_PER_MIN = 50
GLOBAL_RATE_PER_SECOND = GLOBAL_RATE_PER_MIN / 60
GLOBAL_TTL = 3600


async def verify_ip_rate_limiter(
    client: redis.Redis,
    ip_rate_limiter_script_sha: str,
    ip: str,
    endpoint: str,
    ip_bucket_size: int = IP_BUCKET_SIZE,
    ip_rate: float = IP_RATE_PER_SECOND,
    ip_ttl: int = IP_TTL,
    global_bucket_size: int = GLOBAL_BUCKET_SIZE,
    global_rate: float = GLOBAL_RATE_PER_SECOND,
    global_ttl: int = GLOBAL_TTL,
) -> bool:
    ip_key = f"ip_rate_limiter:{ip}:{endpoint}"
    global_key = f"global_rate_limiter:{endpoint}"

    result = client.evalsha(
        ip_rate_limiter_script_sha,
        2,
        ip_key,
        global_key,
        ip_bucket_size,
        ip_rate,
        ip_ttl,
        global_bucket_size,
        global_rate,
        global_ttl,
    )

    if isinstance(result, Awaitable):
        result = await result

    return int(result) == 1
