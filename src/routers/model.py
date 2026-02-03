import asyncio

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from pydantic import BaseModel

from src.middleware.rate_limiter import rate_limiter_middleware
from src.tasks.app import task_queue
from src.tasks.model import image_task, video_task


class TaskResult(BaseModel):
    filepath: str
    content_size: int


router = APIRouter(
    prefix="/model", tags=["Model"], dependencies=[Depends(rate_limiter_middleware)]
)


async def read_file_stream_data(file_streams: list[UploadFile]) -> list[bytes]:
    file_bytes = await asyncio.gather(
        *[file_stream.read() for file_stream in file_streams]
    )
    return list(file_bytes)


@router.post("/images")
async def start_task_image(images: list[UploadFile]) -> dict[str, list[str]]:
    result: list[str] = []

    try:
        file_bytes = await read_file_stream_data(images)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to read image",
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


@router.post("/videos")
async def start_task_video(videos: list[UploadFile]) -> dict[str, list[str]]:
    result: list[str] = []

    try:
        file_bytes = await read_file_stream_data(videos)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to read video",
        )

    for video, file_byte in zip(videos, file_bytes):
        try:
            task_data = video_task.delay(video.filename, file_byte)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service temporarily unavailable",
            )

        result.append(task_data.id)

    return {
        "task_ids": result,
    }


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
