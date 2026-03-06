import logging
import sys
from pathlib import Path

import redis.asyncio as redis


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    return logger

def create_redis_client(host: str, port: int) -> redis.Redis:
    client = redis.Redis(host=host, port=port, db=1)
    return client


async def load_lua_script(client: redis.Redis, path: str) -> str:
    file_data = Path(path).read_text()
    sha: str = await client.script_load(file_data)
    return sha



