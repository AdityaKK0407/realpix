import asyncio

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status, File
from pydantic import BaseModel

from PIL import Image, UnidentifiedImageError

from src.middleware.rate_limiter import rate_limiter_middleware
from src.tasks.app import task_queue
from src.tasks.model import image_task
import io

MAX_IMAGES = 5
MAX_VIDEOS = 2
ALLOWED_IMAGE_EXTENSIONS = ("png", "jpg", "jpeg")
ALLOWED_VIDEO_EXTENSIONS = ()


class TaskResult(BaseModel):
    filepath: str
    content_size: int


router = APIRouter(
    prefix="/model", tags=["Model"], dependencies=[Depends(rate_limiter_middleware)]
)


async def validate_image(
    image: UploadFile, allowed_extensions: tuple[str, ...]
) -> bytes:
    try:
        contents = await image.read()
        img = Image.open(io.BytesIO(contents))
        img.verify()

        img = Image.open(io.BytesIO(contents))
        if not img.format or img.format.lower() not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported image format",
            )
        return contents

    except UnidentifiedImageError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file",
        )

    except Image.DecompressionBombError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image too large or suspicious",
        )

    except OSError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Corrupted or unreadable image file",
        )

    finally:
        await image.seek(0)


@router.post("/images")
async def start_task_image(
    images: list[UploadFile] = File(...),
) -> dict[str, list[str]]:
    max_images: int = MAX_IMAGES
    allowed_extensions: tuple[str, ...] = ALLOWED_IMAGE_EXTENSIONS

    if len(images) > max_images:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Max limit of {max_images} images exceeded",
        )

    result: list[str] = []

    try:
        file_bytes: tuple[bytes, ...] = tuple(
            await asyncio.gather(
                *[validate_image(image, allowed_extensions) for image in images]
            )
        )
    except HTTPException as httpError:
        raise httpError
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process image",
        )

    for image, file_byte in zip(images, file_bytes):
        try:
            task_data = image_task.delay(image.filename, file_byte)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service temporarily unavailable",
            )

        result.append(task_data.id)

    return {
        "task_ids": result,
    }


#
# async def validate_video(video: UploadFile, allowed_extensions: tuple[str]) -> bytes:
#     return await video.read()
#
#
# @router.post("/videos")
# async def start_task_video(
#     videos: list[UploadFile],
#     max_videos: int = MAX_VIDEOS,
#     allowed_extensions: tuple[str] = ALLOWED_VIDEO_EXTENSIONS,
# ) -> dict[str, list[str]]:
#     if len(videos) > max_videos:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f"Max limit of {max_videos} videos exceeded",
#         )
#
#     result: list[str] = []
#
#     try:
#         file_bytes: tuple[bytes] = await asyncio.gather(
#             *[validate_video(video, allowed_extensions) for video in videos]
#         )
#     except HTTPException as httpError:
#         raise httpError
#     except Exception:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Failed to process video",
#         )
#
#     for video, file_byte in zip(videos, file_bytes):
#         try:
#             task_data = video_task.delay(video.filename, file_byte)
#         except HTTPException as httpError:
#             raise httpError
#         except Exception:
#             raise HTTPException(
#                 status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
#                 detail="Service temporarily unavailable",
#             )
#
#         result.append(task_data.id)
#
#     return {
#         "task_ids": result,
#     }


@router.get("/status/{task_id}")
async def check_task_status(task_id: str) -> dict[str, str | TaskResult]:
    task_result = task_queue.AsyncResult(task_id)
    if task_result.state == "SUCCESS":
        try:
            result = TaskResult.model_validate(task_result.result)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected server error",
            )
        return {"status": "completed", "result": result}
    elif task_result.state == "FAILURE":
        return {"status": "failed"}
    else:
        return {"status": "pending"}
