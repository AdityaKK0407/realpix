from unittest.mock import AsyncMock, patch
import uuid
import pytest

from src.redis_client.rate_limiter import (
    create_rate_limiter_token,
    verify_rate_limiter_token,
    activate_rate_limiter_token,
    VerifyTokenResult,
)


@pytest.mark.anyio
async def test_create_rate_limiter_token():
    mock_redis = AsyncMock()
    fixed_uuid = uuid.UUID("12345678-1234-5678-1234-567812345678")

    with patch("src.redis_client.rate_limiter.uuid.uuid4", return_value=fixed_uuid):
        token = await create_rate_limiter_token(mock_redis, "fake_sha", 0, 0, 0)

    assert token == str(fixed_uuid)
    mock_redis.evalsha.assert_awaited_once_with(
        "fake_sha", 1, f"rate_limiter:token:{fixed_uuid}", 0, 0, 0
    )


@pytest.mark.anyio
@pytest.mark.parametrize("test_case", [-1, 0, 1, 2, 3])
async def test_verify_rate_limiter_token(test_case):
    mock_redis = AsyncMock()
    mock_redis.evalsha.return_value = test_case

    result = await verify_rate_limiter_token(mock_redis, "fake_sha", "fake_uuid", 0, 0)

    match test_case:
        case -1:
            assert result == VerifyTokenResult.TOKEN_LIMIT_EXCEEDED
        case 0:
            assert result == VerifyTokenResult.RATE_LIMITED
        case 1:
            assert result == VerifyTokenResult.SUCCESS
        case 2:
            assert result == VerifyTokenResult.INACTIVE_TOKEN
        case 3:
            assert result == VerifyTokenResult.UNREACHABLE

    mock_redis.evalsha.assert_awaited_once_with(
        "fake_sha", 1, f"rate_limiter:token:fake_uuid", 0, 0
    )


@pytest.mark.anyio
async def test_activate_rate_limiter_token():
    mock_redis = AsyncMock()
    mock_redis.evalsha.return_value = 1

    result = await activate_rate_limiter_token(mock_redis, "fake_sha", "fake_uuid")

    assert result == True
    mock_redis.evalsha.assert_awaited_once_with(
        "fake_sha", 1, "rate_limiter:token:fake_uuid"
    )
