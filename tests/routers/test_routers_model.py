from unittest.mock import patch
from fastapi import HTTPException
import pytest
from fastapi import UploadFile
from io import BytesIO
from PIL import Image
from typing import Callable

from dataclasses import dataclass
from src.routers.model import validate_image
from tests.mocks.celery import MockCeleryAsyncResult
from tests.mocks.image import create_image_buffer, create_corrupt_image_buffer


@dataclass
class ValidateImageCaseResult:
    name: str
    save_format: str | None
    buffer_factory: Callable[[str | None], BytesIO]
    allowed_extensions: tuple[str, ...]
    exception: tuple[int, str] | None


VALIDATE_IMAGE_TEST_CASES = [
    ValidateImageCaseResult(
        name="valid image file",
        save_format="PNG",
        buffer_factory=create_image_buffer,
        allowed_extensions=("png",),
        exception=None,
    ),
    ValidateImageCaseResult(
        name="unsupported image file extension",
        save_format="JPEG",
        buffer_factory=create_image_buffer,
        allowed_extensions=("png",),
        exception=(400, "Unsupported image format"),
    ),
    ValidateImageCaseResult(
        name="invalid image",
        save_format=None,
        buffer_factory=lambda _: BytesIO(b"image file"),
        allowed_extensions=("png",),
        exception=(400, "Invalid image file"),
    ),
    ValidateImageCaseResult(
        name="corrupt image",
        save_format="PNG",
        buffer_factory=create_corrupt_image_buffer,
        allowed_extensions=("png",),
        exception=(400, "Corrupted or unreadable image file"),
    ),
]


@pytest.mark.anyio
@pytest.mark.parametrize(
    "test_case", VALIDATE_IMAGE_TEST_CASES, ids=lambda test_case: test_case.name
)
async def test_validate_image(test_case):
    image = UploadFile(
        filename="image.png", file=test_case.buffer_factory(test_case.save_format)
    )

    if test_case.exception:
        with pytest.raises(HTTPException) as e:
            await validate_image(image, test_case.allowed_extensions)

        assert e.value.status_code == test_case.exception[0]
        assert e.value.detail == test_case.exception[1]

    else:
        image_bytes = await validate_image(image, test_case.allowed_extensions)
        assert isinstance(image_bytes, bytes)


@dataclass
class StartTaskCaseResults:
    name: str
    token: str | None
    redis_result: int | None
    no_of_files: int
    expected_status: int


START_TASK_TEST_CASES = [
    StartTaskCaseResults(
        name="missing rate limiter token",
        token=None,
        redis_result=None,
        no_of_files=0,
        expected_status=400,
    ),
    StartTaskCaseResults(
        name="token limit exceeded, key doesn't exist",
        token="abc",
        redis_result=-1,
        no_of_files=0,
        expected_status=401,
    ),
    StartTaskCaseResults(
        name="token limit exceeded, global token count depleted",
        token="abc",
        redis_result=-1,
        no_of_files=0,
        expected_status=401,
    ),
    StartTaskCaseResults(
        name="rate limit exceeded",
        token="abc",
        redis_result=0,
        no_of_files=0,
        expected_status=429,
    ),
    StartTaskCaseResults(
        name="inactive token",
        token="abc",
        redis_result=2,
        no_of_files=0,
        expected_status=403,
    ),
    StartTaskCaseResults(
        name="exceeded number of files limit",
        token="abc",
        redis_result=1,
        no_of_files=6,
        expected_status=400,
    ),
    StartTaskCaseResults(
        name="success case",
        token="abc",
        redis_result=1,
        no_of_files=3,
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

    img = Image.new("RGB", (10, 10), color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    files = [
        ("images", (f"image{i + 1}.png", buffer.getvalue(), "image/png"))
        for i in range(test_case.no_of_files)
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


#
# @pytest.mark.anyio
# @pytest.mark.parametrize(
#     "test_case", START_TASK_TEST_CASES, ids=lambda test_case: test_case.name
# )
# async def test_start_task_video(client, mock_redis_client, test_case):
#     key = f"rate_limiter:token:{test_case.token}"
#     mock_redis_client.store[key] = test_case.redis_result
#
#     headers = {}
#     if test_case.token:
#         headers["X-RateLimit-Token"] = test_case.token
#
#     files = [
#         ("videos", ("a.mp4", b"aaa", "video/mp4")),
#         ("videos", ("b.mp4", b"bbb", "video/mp4")),
#         ("videos", ("c.mp4", b"ccc", "video/mp4")),
#     ]
#
#     response = await client.post(
#         "/model/videos",
#         files=files,
#         headers=headers,
#     )
#
#     assert response.status_code == test_case.expected_status
#
#     if response.status_code == 200:
#         data = response.json()
#         assert isinstance(data, dict)
#         assert isinstance(data["task_ids"], list)
#         for task_id in data["task_ids"]:
#             assert isinstance(task_id, str)
#         assert len(data["task_ids"]) == len(files)


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
