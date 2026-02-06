import pytest
from unittest.mock import patch, AsyncMock
from dataclasses import dataclass
import uuid


@dataclass
class VerifyCaptchaCaseResults:
    name: str
    token_body: str | None
    cloudflare_success: bool
    rate_limiter_token: str | None
    saved_rate_limiter_token: str | None
    redis_result: int
    expected_status: int
    expected_body: dict | None


VERIFY_CAPTCHA_TEST_CASES = [
    VerifyCaptchaCaseResults(
        name="missing captcha token",
        token_body=None,
        cloudflare_success=False,
        rate_limiter_token=None,
        saved_rate_limiter_token=None,
        redis_result=3,
        expected_status=400,
        expected_body=None
    ),
    VerifyCaptchaCaseResults(
        name="invalid captcha token",
        token_body="abc",
        cloudflare_success=False,
        rate_limiter_token=None,
        saved_rate_limiter_token=None,
        redis_result=3,
        expected_status=403,
        expected_body=None
    ),
    VerifyCaptchaCaseResults(
        name="rate limit token exists and activated",
        token_body="abc",
        cloudflare_success=True,
        rate_limiter_token="old_token",
        saved_rate_limiter_token="old_token",
        redis_result=1,
        expected_status=200,
        expected_body={"user_token": "old_token"}
    ),
    VerifyCaptchaCaseResults(
        name="rate limit token exists but failed to activate, returns new token",
        token_body="abc",
        cloudflare_success=True,
        rate_limiter_token="old_token",
        saved_rate_limiter_token=None,
        redis_result=0,
        expected_status=200,
        expected_body={"user_token": "12345678-1234-5678-1234-567812345678"}
    ),
    VerifyCaptchaCaseResults(
        name="missing rate limit token, returns new token",
        token_body="abc",
        cloudflare_success=True,
        rate_limiter_token=None,
        saved_rate_limiter_token=None,
        redis_result=3,
        expected_status=200,
        expected_body={"user_token": "12345678-1234-5678-1234-567812345678"}
    )
]


@pytest.mark.anyio
@pytest.mark.parametrize(
    "test_case",
    VERIFY_CAPTCHA_TEST_CASES,
    ids=lambda test_case: test_case.name
)
async def test_verify_captcha(client, mock_redis_client, test_case):
    key = f"rate_limiter:token:{test_case.saved_rate_limiter_token}"
    mock_redis_client.store[key] = test_case.redis_result

    headers = {}
    if test_case.rate_limiter_token:
        headers["X-RateLimit-Token"] = test_case.rate_limiter_token

    fixed_uuid = uuid.UUID("12345678-1234-5678-1234-567812345678")

    req_body = {"token": test_case.token_body} if test_case.token_body else {}

    with patch("src.routers.verification.verify_turnstile",
               new=AsyncMock(return_value=test_case.cloudflare_success)), patch("src.redis_client.rate_limiter.uuid.uuid4",
                                                                                return_value=fixed_uuid):
        response = await client.post("/verify/captcha", json=req_body, headers=headers)

    assert response.status_code == test_case.expected_status

    if response.status_code == 200:
        data = response.json()
        assert data == test_case.expected_body
