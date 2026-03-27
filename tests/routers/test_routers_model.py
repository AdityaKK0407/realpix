from dataclasses import dataclass
from io import BytesIO
from typing import Callable
from unittest.mock import patch

import pytest
from fastapi import HTTPException, UploadFile
from PIL import Image

from src.routers.model import validate_image, validate_video
from tests.mocks.celery import MockCeleryAsyncResult
from tests.mocks.image import (
    create_corrupt_image_buffer,
    create_image_buffer,
    create_image_buffer_bomb,
    create_large_image_buffer,
)
from tests.mocks.video import (
    create_video,
    create_large_video,
    create_corrupted_video,
    create_invalid_video_stream
)


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
        name="image too large",
        save_format="PNG",
        buffer_factory=create_large_image_buffer,
        allowed_extensions=("png",),
        exception=(400, "Image too large"),
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
        name="image decompression bomb",
        save_format="PNG",
        buffer_factory=create_image_buffer_bomb,
        allowed_extensions=("png",),
        exception=(400, "Dangerous image file"),
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

    max_image_file_size = 5 * 1024 * 1024
    image_chunk_size = 512 * 1024

    if test_case.exception:
        with pytest.raises(HTTPException) as e:
            await validate_image(
                image,
                test_case.allowed_extensions,
                max_image_file_size,
                image_chunk_size,
            )

        assert e.value.status_code == test_case.exception[0]
        assert e.value.detail == test_case.exception[1]

    else:
        image_bytes = await validate_image(
            image, test_case.allowed_extensions, max_image_file_size, image_chunk_size
        )
        assert isinstance(image_bytes, bytes)


@dataclass
class StartImageTaskCaseResults:
    name: str
    token: str | None
    redis_result: int | None
    no_of_files: int
    expected_status: int


START_IMAGE_TASK_TEST_CASES = [
    StartImageTaskCaseResults(
        name="missing rate limiter token",
        token=None,
        redis_result=None,
        no_of_files=0,
        expected_status=400,
    ),
    StartImageTaskCaseResults(
        name="token limit exceeded, key doesn't exist",
        token="fake_token",
        redis_result=-1,
        no_of_files=0,
        expected_status=401,
    ),
    StartImageTaskCaseResults(
        name="token limit exceeded, global token count depleted",
        token="fake_token",
        redis_result=-1,
        no_of_files=0,
        expected_status=401,
    ),
    StartImageTaskCaseResults(
        name="rate limit exceeded",
        token="fake_token",
        redis_result=0,
        no_of_files=0,
        expected_status=429,
    ),
    StartImageTaskCaseResults(
        name="inactive token",
        token="fake_token",
        redis_result=2,
        no_of_files=0,
        expected_status=403,
    ),
    StartImageTaskCaseResults(
        name="exceeded number of files limit",
        token="fake_token",
        redis_result=1,
        no_of_files=6,
        expected_status=400,
    ),
    StartImageTaskCaseResults(
        name="success case",
        token="fake_token",
        redis_result=1,
        no_of_files=3,
        expected_status=200,
    ),
]


@pytest.mark.anyio
@pytest.mark.parametrize(
    "test_case", START_IMAGE_TASK_TEST_CASES, ids=lambda test_case: test_case.name
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
    data = response.json()

    if response.status_code == 200:
        assert isinstance(data, dict)
        assert data["status"] == "success"
        assert isinstance(data["task_id"], str)

    else:
        assert isinstance(data, dict)
        assert data["status"] == "error"
        assert isinstance(data["detail"], str)


@dataclass
class ValidateVideoCaseResult:
    name: str
    filename: str
    duration: int
    extension: str
    codec: str
    resolution: tuple[int, int]
    buffer_factory: Callable[[int, str, tuple[int, int], str], BytesIO]
    allowed_extensions: tuple[str, ...]
    allowed_codecs: tuple[str, ...]
    exception: tuple[int, str] | None


VALIDATE_VIDEO_TEST_CASES = [
    ValidateVideoCaseResult(
        name="valid video file",
        filename="video.mp4",
        duration=10,
        extension="mp4",
        codec="libx264",
        resolution=(640, 480),
        buffer_factory=create_video,
        allowed_extensions=("mp4",),
        allowed_codecs=("h264",),
        exception=None
    ),
    ValidateVideoCaseResult(
        name="video file too large",
        filename="video.mp4",
        duration=5,
        extension="mp4",
        codec="libx264",
        resolution=(640, 480),
        buffer_factory=create_large_video,
        allowed_extensions=("mp4",),
        allowed_codecs=("libx264",),
        exception=(400, "Video too large")
    ),
    ValidateVideoCaseResult(
        name="invalid video extension file",
        filename="video.png",
        duration=5,
        extension="mp4",
        codec="libx264",
        resolution=(640, 480),
        buffer_factory=create_video,
        allowed_extensions=("mp4",),
        allowed_codecs=("h264",),
        exception=(400, "Unsupported video format")
    ),
    ValidateVideoCaseResult(
        name="invalid or corrupted video file",
        filename="video.mp4",
        duration=5,
        extension="mp4",
        codec="libx264",
        resolution=(640, 480),
        buffer_factory=create_corrupted_video,
        allowed_extensions=("mp4",),
        allowed_codecs=("h264",),
        exception=(400, "Invalid or corrupted video")
    ),
    ValidateVideoCaseResult(
        name="invalid video stream file",
        filename="video.mp4",
        duration=5,
        extension="mp4",
        codec="aac",
        resolution=(0, 0),
        buffer_factory=create_invalid_video_stream,
        allowed_extensions=("mp4",),
        allowed_codecs=("h264",),
        exception=(400, "No video stream found")
    ),
    ValidateVideoCaseResult(
        name="unsupported video extension file",
        filename="video.webm",
        duration=5,
        extension="mp4",
        codec="libx264",
        resolution=(640, 480),
        buffer_factory=create_video,
        allowed_extensions=("webm",),
        allowed_codecs=("h264",),
        exception=(400, "Unsupported video format")
    ),
    ValidateVideoCaseResult(
        name="unsupported video codec file",
        filename="video.mp4",
        duration=5,
        extension="mp4",
        codec="libx264",
        resolution=(640, 480),
        buffer_factory=create_video,
        allowed_extensions=("mp4",),
        allowed_codecs=tuple(),
        exception=(400, "Unsupported codec")
    ),
    ValidateVideoCaseResult(
        name="too large resolution",
        filename="video.mp4",
        duration=5,
        extension="mp4",
        codec="libx264",
        resolution=(2000, 1100),
        buffer_factory=create_video,
        allowed_extensions=("mp4",),
        allowed_codecs=("h264",),
        exception=(400, "Resolution too high")
    ),
    ValidateVideoCaseResult(
        name="too long duration",
        filename="video.mp4",
        duration=35,
        extension="mp4",
        codec="libx264",
        resolution=(640, 480),
        buffer_factory=create_video,
        allowed_extensions=("mp4",),
        allowed_codecs=("h264",),
        exception=(400, "Video too long")
    ),
]


@pytest.mark.anyio
@pytest.mark.parametrize(
    "test_case", VALIDATE_VIDEO_TEST_CASES, ids=lambda test_case: test_case.name
)
async def test_validate_video(test_case):
    video = UploadFile(
        filename=test_case.filename,
        file=test_case.buffer_factory(test_case.duration, test_case.codec, test_case.resolution, test_case.extension)
    )

    max_video_file_size = 5 * 1024 * 1024
    video_chunk_size = 512 * 1024

    if test_case.exception:
        with pytest.raises(HTTPException) as e:
            await validate_video(
                video,
                test_case.allowed_extensions,
                max_video_file_size,
                video_chunk_size,
                test_case.allowed_codecs,
            )

        assert e.value.status_code == test_case.exception[0]
        assert e.value.detail == test_case.exception[1]

    else:
        video_bytes = await validate_video(
            video, test_case.allowed_extensions, max_video_file_size, video_chunk_size, test_case.allowed_codecs
        )
        assert isinstance(video_bytes, bytes)


@dataclass
class StartVideoTaskCaseResults:
    name: str
    token: str | None
    redis_result: int | None
    no_of_files: int
    expected_status: int


START_VIDEO_TASK_TEST_CASES = [
    StartVideoTaskCaseResults(
        name="missing rate limiter token",
        token=None,
        redis_result=None,
        no_of_files=0,
        expected_status=400,
    ),
    StartVideoTaskCaseResults(
        name="token limit exceeded, key doesn't exist",
        token="fake_token",
        redis_result=-1,
        no_of_files=0,
        expected_status=401,
    ),
    StartVideoTaskCaseResults(
        name="token limit exceeded, global token count depleted",
        token="fake_token",
        redis_result=-1,
        no_of_files=0,
        expected_status=401,
    ),
    StartVideoTaskCaseResults(
        name="rate limit exceeded",
        token="fake_token",
        redis_result=0,
        no_of_files=0,
        expected_status=429,
    ),
    StartVideoTaskCaseResults(
        name="inactive token",
        token="fake_token",
        redis_result=2,
        no_of_files=0,
        expected_status=403,
    ),
    StartVideoTaskCaseResults(
        name="exceeded number of files limit",
        token="fake_token",
        redis_result=1,
        no_of_files=2,
        expected_status=400,
    ),
    StartVideoTaskCaseResults(
        name="success case",
        token="fake_token",
        redis_result=1,
        no_of_files=1,
        expected_status=200,
    ),
]


@pytest.mark.anyio
@pytest.mark.parametrize(
    "test_case", START_VIDEO_TASK_TEST_CASES, ids=lambda test_case: test_case.name
)
async def test_start_task_video(client, mock_redis_client, test_case):
    key = f"rate_limiter:token:{test_case.token}"
    mock_redis_client.store[key] = test_case.redis_result

    headers = {}
    if test_case.token:
        headers["X-RateLimit-Token"] = test_case.token

    files = [
        ("videos", (f"video{i + 1}.mp4", create_video(5, "libx264", (640, 480), "mp4").getvalue(), "video/mp4"))
        for i in range(test_case.no_of_files)
    ]

    response = await client.post(
        "/model/videos",
        files=files,
        headers=headers,
    )

    assert response.status_code == test_case.expected_status
    data = response.json()

    if response.status_code == 200:
        assert isinstance(data, dict)
        assert data["status"] == "success"
        assert isinstance(data["task_id"], str)

    else:
        assert isinstance(data, dict)
        assert data["status"] == "error"
        assert isinstance(data["detail"], str)


@dataclass
class CheckTaskCaseResults:
    name: str
    token: str | None
    redis_result: int | None
    expected_status: int
    state: str | None
    result_state: str | None


CHECK_TASK_TEST_CASES = [
    CheckTaskCaseResults(
        name="missing rate limiter token",
        token=None,
        redis_result=None,
        expected_status=400,
        state=None,
        result_state=None
    ),
    CheckTaskCaseResults(
        name="token limit exceeded, key doesn't exist",
        token="fake_token",
        redis_result=-1,
        expected_status=401,
        state=None,
        result_state=None
    ),
    CheckTaskCaseResults(
        name="token limit exceeded, global token count depleted",
        token="fake_token",
        redis_result=-1,
        expected_status=401,
        state=None,
        result_state=None
    ),
    CheckTaskCaseResults(
        name="rate limit exceeded",
        token="fake_token",
        redis_result=0,
        expected_status=429,
        state=None,
        result_state=None
    ),
    CheckTaskCaseResults(
        name="inactive token",
        token="fake_token",
        redis_result=2,
        expected_status=403,
        state=None,
        result_state=None
    ),
    CheckTaskCaseResults(
        name="success case, status complete",
        token="fake_token",
        redis_result=1,
        expected_status=200,
        state="SUCCESS",
        result_state="completed"
    ),
    CheckTaskCaseResults(
        name="success case, status failed",
        token="fake_token",
        redis_result=1,
        expected_status=200,
        state="FAILURE",
        result_state="failed"
    ),
    CheckTaskCaseResults(
        name="success case, status pending",
        token="fake_token",
        redis_result=1,
        expected_status=200,
        state="PENDING",
        result_state="pending"
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
            return_value=MockCeleryAsyncResult(test_case.state, [True, False, True]),
    ):
        response = await client.get(
            "/model/status/fake_task_id",
            headers=headers,
        )

    assert response.status_code == test_case.expected_status
    data = response.json()

    if response.status_code == 200:
        assert isinstance(data, dict)
        assert data["status"] == "success"
        assert data["result"] == test_case.result_state
        if test_case.result_state == "completed":
            assert isinstance(data["data"], list)
            for item in data["data"]:
                assert isinstance(item, bool)


    else:
        assert isinstance(data, dict)
        assert data["status"] == "error"
        assert isinstance(data["detail"], str)
