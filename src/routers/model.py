import asyncio
import io
import json
import logging
import os
import subprocess
import tempfile
from typing import Any

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from PIL import Image, UnidentifiedImageError

from src.middleware.rate_limiter import rate_limiter_middleware
from src.tasks.app import task_queue
from src.tasks.model import image_task, video_task

logger = logging.getLogger(__name__)

MAX_IMAGES = 5
ALLOWED_IMAGE_EXTENSIONS = ("png", "jpg", "jpeg")
MAX_IMAGE_FILE_SIZE = 5 * 1024 * 1024
IMAGE_CHUNK_SIZE = 512 * 1024

MAX_VIDEOS = 1
ALLOWED_VIDEO_EXTENSIONS = ("mp4",)
MAX_VIDEO_FILE_SIZE = 50 * 1024 * 1024
VIDEO_CHUNK_SIZE = 1024 * 1024
ALLOWED_CODECS = ("h264",)

router = APIRouter(
    prefix="/model", tags=["Model"], dependencies=[Depends(rate_limiter_middleware)]
)


async def validate_image(
    image: UploadFile,
    allowed_extensions: tuple[str, ...],
    max_image_file_size: int,
    image_chunk_size: int,
) -> bytes:
    try:
        contents = bytearray()
        while True:
            chunk = await image.read(image_chunk_size)
            if not chunk:
                break
            contents.extend(chunk)
            if len(contents) > max_image_file_size:
                logger.warning("Image file provided is too large")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Image too large"
                )
        img = Image.open(io.BytesIO(contents))
        img.verify()

        img = Image.open(io.BytesIO(contents))
        if not img.format or img.format.lower() not in allowed_extensions:
            logger.warning("Invalid image extension format provided")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported image format",
            )
        return bytes(contents)

    except UnidentifiedImageError:
        logger.warning("Invalid image file provided")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file",
        )

    except Image.DecompressionBombError:
        logger.warning("Provided image is potentially a decompression bomb")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dangerous image file",
        )

    except OSError:
        logger.warning("Corrupted or unreadable image file")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Corrupted or unreadable image file",
        )

    finally:
        await image.seek(0)


@router.post("/images", response_model=None)
async def start_task_image(
    images: list[UploadFile] = File(...),
) -> dict[str, str]:
    max_images = MAX_IMAGES
    allowed_extensions: tuple[str, ...] = ALLOWED_IMAGE_EXTENSIONS
    max_image_file_size = MAX_IMAGE_FILE_SIZE
    image_chunk_size = IMAGE_CHUNK_SIZE

    if len(images) < 1:
        logger.warning("Client didn't provide any images")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one image must be provided",
        )

    if len(images) > max_images:
        logger.warning("Client provided too many images")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Max limit of {max_images} images exceeded",
        )

    try:
        file_bytes: tuple[bytes, ...] = tuple(
            await asyncio.gather(
                *[
                    validate_image(
                        image, allowed_extensions, max_image_file_size, image_chunk_size
                    )
                    for image in images
                ]
            )
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Server failed to process the images: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process image",
        )

    try:
        result: str = image_task.delay(file_bytes).id
    except Exception as e:
        logger.error(f"Celery task failed to add images to task queue: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service temporarily unavailable",
        )

    return {
        "status": "success",
        "task_id": result,
    }


async def validate_video(
    video: UploadFile,
    allowed_extensions: tuple[str, ...],
    max_video_file_size: int,
    video_chunk_size: int,
    allowed_codecs: tuple[str, ...],
) -> bytes:
    contents = bytearray()
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        while True:
            chunk = await video.read(video_chunk_size)
            if not chunk:
                break
            contents.extend(chunk)
            if len(contents) > max_video_file_size:
                tmp.close()
                os.remove(tmp.name)
                logger.warning("Video file provided is too large")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Video too large"
                )
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        if not video.filename:
            logger.critical("UploadFile must have filename attribute")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected server error",
            )
        ext = video.filename.split(".")[-1].lower()
        if ext not in allowed_extensions:
            logger.warning("Invalid video extension format provided")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported video format",
            )

        cmd = [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=codec_name,width,height,r_frame_rate:format=duration,format_name",
            "-of",
            "json",
            tmp_path,
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            logger.warning("Video file provided was invalid or corrupted")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or corrupted video",
            )

        data: dict[str, Any] = json.loads(result.stdout)

        if "streams" not in data or len(data["streams"]) == 0:
            logger.warning("Provided file does not contain a valid video stream")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="No video stream found"
            )

        format_names: str = data["format"]["format_name"].lower().split(",")
        if not any(fmt in allowed_extensions for fmt in format_names):
            logger.warning("Provided video file container is not supported")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported video format",
            )

        stream: dict[str, Any] = data["streams"][0]
        codec: str = stream["codec_name"]
        width: int = stream["width"]
        height: int = stream["height"]
        duration = float(data["format"]["duration"])

        if codec not in allowed_codecs:
            logger.warning(f"Client provided codec {codec} which is not allowed")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported codec",
            )

        if width > 1920 or height > 1080:
            logger.warning("Client provided video with too large resolution")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Resolution too high"
            )

        if duration > 30:
            logger.warning(
                f"Video duration of {duration} exceeds max limit of 30 seconds"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Video too long"
            )
        return bytes(contents)
    finally:
        os.remove(tmp_path)


@router.post("/videos", response_model=None)
async def start_task_video(
    videos: list[UploadFile] = File(...),
) -> dict[str, str]:
    max_videos = MAX_VIDEOS
    allowed_extensions = ALLOWED_VIDEO_EXTENSIONS
    max_video_file_size = MAX_VIDEO_FILE_SIZE
    video_chunk_size = VIDEO_CHUNK_SIZE
    allowed_codecs = ALLOWED_CODECS

    if len(videos) < 1:
        logger.warning("Client didn't provide any videos")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one video must be provided",
        )

    if len(videos) > max_videos:
        logger.warning("Client provided too many videos")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Max limit of {max_videos} videos exceeded",
        )

    try:
        file_bytes: tuple[bytes, ...] = tuple(
            await asyncio.gather(
                *[
                    validate_video(
                        video,
                        allowed_extensions,
                        max_video_file_size,
                        video_chunk_size,
                        allowed_codecs,
                    )
                    for video in videos
                ]
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Server failed to process the videos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process video",
        )

    try:
        result: str = video_task.delay(file_bytes).id
    except Exception as e:
        logger.error(f"Celery task failed to add videos to task queue: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service temporarily unavailable",
        )

    return {
        "status": "success",
        "task_id": result,
    }


@router.get("/status/{task_id}", response_model=None)
async def check_task_status(task_id: str) -> dict[str, str | list[bool]]:
    try:
        task_result = task_queue.AsyncResult(task_id)
    except Exception as e:
        logger.error(f"Celery task failed to get status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error",
        )
    if task_result.state == "SUCCESS":
        model_result: list[bool] = task_result.result
        return {"status": "success", "result": "completed", "data": model_result}
    elif task_result.state == "FAILURE":
        return {"status": "success", "result": "failed"}
    else:
        return {"status": "success", "result": "pending"}
