from src.celery_app import task_queue
from src.tasks import image_task, video_task
from fastapi import FastAPI, UploadFile
from pydantic import BaseModel

class TurnStileToken(BaseModel):
    token: str

app = FastAPI()


@app.get("/")
def home():
    return {"status": "running"}

@app.post("/start-task-image")
async def start_task_image(image: UploadFile):
    content = await image.read()
    task_data = image_task.delay(image.filename, content)
    return {
        "task_id": task_data.id,
        "name": image.filename
    }


@app.post("verify-captcha")
async def verify_captcha(turnstile_token: TurnStileToken):
    pass

@app.post("/start-task-video")
async def start_task_video(video: UploadFile):
    content = await video.read()
    task_data = video_task.delay(video.filename, content)
    return {
        "task_id": task_data.id,
        "name": video.filename
    }

@app.get("/task-status/{task_id}")
async def check_task_status(task_id: str):
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
