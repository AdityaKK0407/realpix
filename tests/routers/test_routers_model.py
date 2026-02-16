from unittest.mock import patch

import pytest
from fastapi import UploadFile
from io import BytesIO

from dataclasses import dataclass
from src.routers.model import validate_image
from tests.mocks.celery import MockCeleryAsyncResult


@pytest.mark.anyio
async def test_validate_image():
    images = [
        UploadFile(
            filename="a.png",
            file=BytesIO(b"aaa"),
        ),
        UploadFile(
            filename="b.png",
            file=BytesIO(b"bbb"),
        ),
        UploadFile(
            filename="c.png",
            file=BytesIO(b"ccc"),
        ),
    ]

    for image in images:
        image_bytes = await validate_image(image, (".png",))
        assert (image_bytes, bytes)


@dataclass
class StartTaskCaseResults:
    name: str
    token: str | None
    redis_result: int | None
    expected_status: int


START_TASK_TEST_CASES = [
    StartTaskCaseResults(
        name="missing rate limiter token",
        token=None,
        redis_result=None,
        expected_status=400,
    ),
    StartTaskCaseResults(
        name="token limit exceeded, key doesn't exist",
        token="abc",
        redis_result=-1,
        expected_status=401,
    ),
    StartTaskCaseResults(
        name="token limit exceeded, global token count depleted",
        token="abc",
        redis_result=-1,
        expected_status=401,
    ),
    StartTaskCaseResults(
        name="rate limit exceeded",
        token="abc",
        redis_result=0,
        expected_status=429,
    ),
    StartTaskCaseResults(
        name="inactive token",
        token="abc",
        redis_result=2,
        expected_status=403,
    ),
    StartTaskCaseResults(
        name="success case",
        token="abc",
        redis_result=1,
        expected_status=200,
    ),
]


@pytest.mark.anyio
@pytest.mark.parametrize(
    "test_case", START_TASK_TEST_CASES, ids=lambda test_case: test_case.name
)
async def test_start_task_image(client, mock_redis_client, test_case):
    key = f"rate_limiter:token:{test_case.token}"
    mock_redis_client.store[key] = test_case.redis_result

    headers = {}
    if test_case.token:
        headers["X-RateLimit-Token"] = test_case.token

    files = [
        ("images", ("a.png", b"aaa", "image/png")),
        ("images", ("b.png", b"bbb", "image/png")),
        ("images", ("c.png", b"ccc", "image/png")),
    ]

    response = await client.post(
        "/model/images",
        files=files,
        headers=headers,
    )

    assert response.status_code == test_case.expected_status

    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, dict)
        assert isinstance(data["task_ids"], list)
        for task_id in data["task_ids"]:
            assert isinstance(task_id, str)
        assert len(data["task_ids"]) == len(files)


@pytest.mark.anyio
@pytest.mark.parametrize(
    "test_case", START_TASK_TEST_CASES, ids=lambda test_case: test_case.name
)
async def test_start_task_video(client, mock_redis_client, test_case):
    key = f"rate_limiter:token:{test_case.token}"
    mock_redis_client.store[key] = test_case.redis_result

    headers = {}
    if test_case.token:
        headers["X-RateLimit-Token"] = test_case.token

    files = [
        ("videos", ("a.mp4", b"aaa", "video/mp4")),
        ("videos", ("b.mp4", b"bbb", "video/mp4")),
        ("videos", ("c.mp4", b"ccc", "video/mp4")),
    ]

    response = await client.post(
        "/model/videos",
        files=files,
        headers=headers,
    )

    assert response.status_code == test_case.expected_status

    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, dict)
        assert isinstance(data["task_ids"], list)
        for task_id in data["task_ids"]:
            assert isinstance(task_id, str)
        assert len(data["task_ids"]) == len(files)


@dataclass
class CheckTaskCaseResults:
    name: str
    token: str | None
    redis_result: int | None
    expected_status: int
    state: str | None
    result: dict | None
    expected_body: dict | None


CHECK_TASK_TEST_CASES = [
    CheckTaskCaseResults(
        name="missing rate limiter token",
        token=None,
        redis_result=None,
        expected_status=400,
        state=None,
        result=None,
        expected_body=None,
    ),
    CheckTaskCaseResults(
        name="token limit exceeded, key doesn't exist",
        token="abc",
        redis_result=-1,
        expected_status=401,
        state=None,
        result=None,
        expected_body=None,
    ),
    CheckTaskCaseResults(
        name="token limit exceeded, global token count depleted",
        token="abc",
        redis_result=-1,
        expected_status=401,
        state=None,
        result=None,
        expected_body=None,
    ),
    CheckTaskCaseResults(
        name="rate limit exceeded",
        token="abc",
        redis_result=0,
        expected_status=429,
        state=None,
        result=None,
        expected_body=None,
    ),
    CheckTaskCaseResults(
        name="inactive token",
        token="abc",
        redis_result=2,
        expected_status=403,
        state=None,
        result=None,
        expected_body=None,
    ),
    CheckTaskCaseResults(
        name="success case, status complete",
        token="abc",
        redis_result=1,
        expected_status=200,
        state="SUCCESS",
        result={"filepath": "", "content_size": 0},
        expected_body={
            "status": "completed",
            "result": {"filepath": "", "content_size": 0},
        },
    ),
    CheckTaskCaseResults(
        name="success case, status failed",
        token="abc",
        redis_result=1,
        expected_status=200,
        state="FAILURE",
        result=None,
        expected_body={"status": "failed"},
    ),
    CheckTaskCaseResults(
        name="success case, status pending",
        token="abc",
        redis_result=1,
        expected_status=200,
        state="PENDING",
        result=None,
        expected_body={"status": "pending"},
    ),
]


@pytest.mark.anyio
@pytest.mark.parametrize(
    "test_case", CHECK_TASK_TEST_CASES, ids=lambda test_case: test_case.name
)
async def test_check_task_status(client, mock_redis_client, test_case):
    key = f"rate_limiter:token:{test_case.token}"
    mock_redis_client.store[key] = test_case.redis_result

    headers = {}
    if test_case.token:
        headers["X-RateLimit-Token"] = test_case.token

    with patch(
        "src.routers.model.task_queue.AsyncResult",
        return_value=MockCeleryAsyncResult(test_case.state, test_case.result),
    ):
        response = await client.get(
            "/model/status/fake_task_id",
            headers=headers,
        )

    assert response.status_code == test_case.expected_status

    if response.status_code == 200:
        data = response.json()
        assert test_case.expected_body == data
