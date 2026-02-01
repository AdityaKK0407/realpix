import redis
from pathlib import Path

def create_redis_client(host: str, port: int) -> redis.Redis:
    client = redis.Redis(host=host, port=port, db=1)
    return client

def load_lua_script(client: redis.Redis, path: str) -> str:
    file_data = Path(path).read_text()
    return client.script_load(file_data)