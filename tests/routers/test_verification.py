from dataclasses import dataclass
from unittest.mock import AsyncMock, patch

import pytest


@dataclass
class VerifyCaptchaCaseResults:
    name: str
    token_body: str | None
    cloudflare_success: bool
    client_ip: str | None
    rate_limiter_token: str | None
    saved_rate_limiter_token: str | None
    redis_result: int
    expected_status: int


VERIFY_CAPTCHA_TEST_CASES = [
    VerifyCaptchaCaseResults(
        name="missing captcha token",
        token_body=None,
        client_ip=None,
        cloudflare_success=False,
        rate_limiter_token=None,
        saved_rate_limiter_token=None,
        redis_result=3,
        expected_status=400,
    ),
    VerifyCaptchaCaseResults(
        name="missing client ip",
        token_body="fake_turnstile_token",
        client_ip=None,
        cloudflare_success=False,
        rate_limiter_token=None,
        saved_rate_limiter_token=None,
        redis_result=3,
        expected_status=400,
    ),
    VerifyCaptchaCaseResults(
        name="invalid captcha token",
        token_body="fake_turnstile_token",
        client_ip="fake_client_ip",
        cloudflare_success=False,
        rate_limiter_token=None,
        saved_rate_limiter_token=None,
        redis_result=3,
        expected_status=403,
    ),
    VerifyCaptchaCaseResults(
        name="rate limit token exists and activated",
        token_body="fake_turnstile_token",
        client_ip="fake_client_ip",
        cloudflare_success=True,
        rate_limiter_token="old_token",
        saved_rate_limiter_token="old_token",
        redis_result=1,
        expected_status=200,
    ),
    VerifyCaptchaCaseResults(
        name="rate limit token exists but failed to activate, returns new token",
        token_body="fake_turnstile_token",
        client_ip="fake_client_ip",
        cloudflare_success=True,
        rate_limiter_token="old_token",
        saved_rate_limiter_token=None,
        redis_result=0,
        expected_status=200,
    ),
    VerifyCaptchaCaseResults(
        name="missing rate limit token, returns new token",
        token_body="fake_turnstile_token",
        client_ip="fake_client_ip",
        cloudflare_success=True,
        rate_limiter_token=None,
        saved_rate_limiter_token=None,
        redis_result=3,
        expected_status=200,
    ),
]


@pytest.mark.anyio
@pytest.mark.parametrize(
    "test_case", VERIFY_CAPTCHA_TEST_CASES, ids=lambda test_case: test_case.name
)
async def test_verify_captcha(client, mock_redis_client, test_case):
    key = f"rate_limiter:token:{test_case.saved_rate_limiter_token}"
    mock_redis_client.store[key] = test_case.redis_result

    headers = {}
    if test_case.client_ip:
        headers["X-Client-Ip"] = test_case.client_ip
    if test_case.rate_limiter_token:
        headers["X-RateLimit-Token"] = test_case.rate_limiter_token

    req_body = {"token": test_case.token_body} if test_case.token_body else {}

    with patch("src.routers.verification.verify_turnstile", new=AsyncMock(return_value=test_case.cloudflare_success)):
        response = await client.post("/verify/captcha", json=req_body, headers=headers)

    assert response.status_code == test_case.expected_status
    data = response.json()

    if response.status_code == 200:
        assert isinstance(data, dict)
        assert data["status"] == "success"
        assert isinstance (data["user_token"], str)

    else:
        assert isinstance(data, dict)
        assert data["status"] == "error"
        assert isinstance (data["detail"], str)

