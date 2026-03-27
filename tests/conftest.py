import uuid
from unittest.mock import patch

import pytest
from httpx import ASGITransport, AsyncClient

from src.dependencies import (
    get_activate_token_sha,
    get_create_sha,
    get_ip_rate_limiter_sha,
    get_redis,
    get_verify_sha,
)
from src.main import app
from tests.mocks.celery import MockCelery
from tests.mocks.redis import MockRedis


@pytest.fixture
async def client():
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client


@pytest.fixture
def mock_redis_client():
    return MockRedis()


@pytest.fixture(autouse=True)
def mock_celery():
    with (
        patch("src.routers.model.image_task.delay") as mock_image_delay,
        patch("src.routers.model.video_task.delay") as mock_video_delay,
    ):
        mock_image_delay.side_effect = lambda *args, **kwargs: MockCelery(
            str(uuid.uuid4())
        )
        mock_video_delay.side_effect = lambda *args, **kwargs: MockCelery(
            str(uuid.uuid4())
        )
        yield mock_image_delay, mock_video_delay


@pytest.fixture
def mock_create_sha():
    return "create"


@pytest.fixture
def mock_verify_sha():
    return "verify"


@pytest.fixture
def mock_activate_token_sha():
    return "activate_token"


@pytest.fixture
def mock_ip_rate_limiter_sha():
    return "ip_rate_limiter"


@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    monkeypatch.setenv("CLOUDFLARE_URL", "cloudflare_url")
    monkeypatch.setenv("CLOUDFLARE_SECRET_KEY", "secret_key")
    monkeypatch.setenv("REDIS_HOST", "redis_host")
    monkeypatch.setenv("REDIS_PORT", "redis_port")
    monkeypatch.setenv("PYTHON_UNBUFFERED", "true")
    monkeypatch.setenv("LOG_LEVEL", "log_level")
    monkeypatch.setenv("SERVER", "development")


@pytest.fixture(autouse=True)
def override_dependencies(
    mock_redis_client,
    mock_create_sha,
    mock_verify_sha,
    mock_activate_token_sha,
    mock_ip_rate_limiter_sha,
):
    app.dependency_overrides[get_redis] = lambda: mock_redis_client
    app.dependency_overrides[get_create_sha] = lambda: mock_create_sha
    app.dependency_overrides[get_verify_sha] = lambda: mock_verify_sha
    app.dependency_overrides[get_activate_token_sha] = lambda: mock_activate_token_sha
    app.dependency_overrides[get_ip_rate_limiter_sha] = lambda: mock_ip_rate_limiter_sha
    yield
    app.dependency_overrides.clear()
