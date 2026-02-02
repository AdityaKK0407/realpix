from fastapi import APIRouter, Depends, UploadFile, HTTPException, status
from typing import cast, Any
from src.tasks.model import image_task, video_task
from src.tasks.app import task_queue
from src.middleware.rate_limiter import rate_limiter_middleware

router = APIRouter(
    prefix="/model",
    tags=["Model"],
    dependencies=[Depends(rate_limiter_middleware)]
)


@router.post("/images")
async def start_task_image(images: list[UploadFile]) -> dict[str, list[str]]:
    result: list[str] = [""] * len(images)

    for index, image in enumerate(images):
        try:
            content = await image.read()
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to read image"
            )
        try:
            task_data = image_task.delay(image.filename, content)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service temporarily unavailable"
            )

        result[index] = task_data.id

    return {
        "task_ids": result,
    }


@router.post("/videos")
async def start_task_video(videos: list[UploadFile]) -> dict[str, list[str]]:
    result: list[str] = [""] * len(videos)

    for index, video in enumerate(videos):
        try:
            content = await video.read()
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to read video"
            )

        try:
            task_data = video_task.delay(video.filename, content)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service temporarily unavailable"
            )
        result[index] = task_data.id

    return {
        "task_ids": result,
    }


@router.get("/status/{task_id}")
async def check_task_status(task_id: str) -> dict[str, str | dict[str, str | int]]:
    task_result = task_queue.AsyncResult(task_id)
    if task_result.state == "SUCCESS":
        return {
            "status": "completed",
            "result": cast(dict[str, str | int], task_result.result)
        }
    elif task_result.state == "FAILURE":
        return {"status": "failed"}
    else:
        return {"status": "pending"}
