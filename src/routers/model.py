from fastapi import APIRouter, Request, Depends, UploadFile

from src.model import image_task, video_task
from src.celery_app import task_queue
from src.routers.middleware import rate_limiter_middleware

router = APIRouter(
    prefix="/model",
    tags=["Model"],
    dependencies=[Depends(rate_limiter_middleware)]
)


@router.post("/images")
async def start_task_image(images: list[UploadFile]) -> list[dict[str, str]]:
    result: list[dict | None] = [None] * len(images)

    for index, image in enumerate(images):
        content = await image.read()
        task_data = image_task.delay(image.filename, content)
        result[index] = {"task_id": task_data.id}

    return result


@router.post("/videos")
async def start_task_video(videos: list[UploadFile]) -> list[dict[str, str]]:
    result: list[dict | None] = [None] * len(videos)

    for index, video in enumerate(videos):
        content = await video.read()
        task_data = video_task.delay(video.filename, content)
        result[index] = {"task_id": task_data.id}

    return result


@router.get("/status/{task_id}")
async def check_task_status(task_id: str) -> dict:
    task_result = task_queue.AsyncResult(task_id)
    if task_result.state == "SUCCESS":
        return {
            "status": "completed",
            "result": task_result.result
        }
    elif task_result.state == "FAILED":
        return {"status": "failed"}
    else:
        return {"status": "pending"}
