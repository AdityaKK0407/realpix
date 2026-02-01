from fastapi import Request
import redis

def get_redis(request: Request) -> redis.Redis:
    return request.app.state.redis_client

def get_create_sha(request: Request) -> str:
    return request.app.state.create_sha

def get_verify_sha(request: Request) -> str:
    return request.app.state.verify_sha
