import redis
from pathlib import Path
import uuid

TOTAL_QUOTA = 100
BUCKET_SIZE = 10
RATE_PER_MIN = 2
RATE_PER_SECOND = RATE_PER_MIN / 60
TTL_SECONDS = 30 * 24 * 60 * 60

def create_redis_client():
    client = redis.Redis(host='localhost', port=6379, db=1)
    return client


def load_lua_script(client: redis.Redis, path: str):
    file_data = Path(path).read_text()
    return client.script_load(file_data)


redis_client = create_redis_client()
create_sha = load_lua_script(redis_client, '.redis_scripts/create.lua')
verify_sha = load_lua_script(redis_client, '.redis_scripts/verify.lua')


def create_rate_limiter_token(client: redis.Redis, lua_script_sha):
    token_id = uuid.uuid4()
    key = f'rate_limiter:token:{token_id}'

    initial_tokens = BUCKET_SIZE

    client.evalsha(
        lua_script_sha,
        1,
        key,
        TOTAL_QUOTA,
        initial_tokens,
        TTL_SECONDS
    )

    return token_id


def verify_rate_limiter_token(client: redis.Redis, lua_script_sha, uuid_key: str) -> bool:
    key = f'rate_limiter:token:{uuid_key}'

    result = client.evalsha(
        lua_script_sha,
        1,
        key,
        BUCKET_SIZE,
        RATE_PER_SECOND
    )
    return result == 1