import redis
from fastapi import Request
from typing import cast


def get_redis(request: Request) -> redis.Redis:
    return cast(redis.Redis, request.app.state.redis_client)


def get_create_sha(request: Request) -> str:
    return cast(str, request.app.state.create_sha)


def get_verify_sha(request: Request) -> str:
    return cast(str, request.app.state.verify_sha)


def get_activate_token_sha(request: Request) -> str:
    return cast(str, request.app.state.activate_token_sha)
