import redis
from fastapi import Request


def get_redis(request: Request) -> redis.Redis:
    redis_client: redis.Redis = request.app.state.redis_client
    return redis_client


def get_create_sha(request: Request) -> str:
    create_sha: str = request.app.state.create_sha
    return create_sha


def get_verify_sha(request: Request) -> str:
    verify_sha: str = request.app.state.verify_sha
    return verify_sha


def get_activate_token_sha(request: Request) -> str:
    activate_sha: str = request.app.state.activate_token_sha
    return activate_sha
