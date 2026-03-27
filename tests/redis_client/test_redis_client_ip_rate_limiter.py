from unittest.mock import AsyncMock

import pytest

from src.redis_client.ip_rate_limiter import verify_ip_rate_limiter


@pytest.mark.anyio
async def test_verify_ip_rate_limiter() -> None:
    mock_redis = AsyncMock()
    mock_redis.evalsha.return_value = 1

    result = await verify_ip_rate_limiter(
        mock_redis, "fake_sha", "fake_ip", "fake_endpoint", 0, 0, 0, 0, 0, 0
    )
    assert result

    mock_redis.evalsha.assert_awaited_once_with(
        "fake_sha",
        2,
        "ip_rate_limiter:fake_ip:fake_endpoint",
        "global_rate_limiter:fake_endpoint",
        0,
        0,
        0,
        0,
        0,
        0,
    )
