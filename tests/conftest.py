from unittest.mock import patch
import uuid
import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app
from tests.mocks.redis import MockRedis
from tests.mocks.celery import MockCelery, MockCeleryAsyncResult
from src.dependencies import (
    get_redis,
    get_create_sha,
    get_verify_sha,
    get_activate_token_sha,
)


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
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


@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    monkeypatch.setenv("CLOUDFLARE_URL", "Cloudflare_URL")
    monkeypatch.setenv("CLOUDFLARE_SECRET_KEY", "Secret key")

@pytest.fixture(autouse=True)
def override_dependencies(
    mock_redis_client, mock_create_sha, mock_verify_sha, mock_activate_token_sha
):
    app.dependency_overrides[get_redis] = lambda: mock_redis_client
    app.dependency_overrides[get_create_sha] = lambda: mock_create_sha
    app.dependency_overrides[get_verify_sha] = lambda: mock_verify_sha
    app.dependency_overrides[get_activate_token_sha] = lambda: mock_activate_token_sha
    yield
    app.dependency_overrides.clear()
