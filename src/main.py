from fastapi import FastAPI
from src.tasks import long_running_task
from src.celery_app import celery_app

app = FastAPI()


@app.get("/")
def home():
    return {"status": "running"}


@app.post("/start-task")
async def start_task(x: int):
    task = long_running_task.delay(x)
    return {
        "task_id": task.id,
    }


@app.get("/task-status/{task_id}")
async def check_task_status(task_id: str):
    task_result = celery_app.AsyncResult(task_id)
    if task_result.state == "SUCCESS":
        return {
            "status": "completed",
            "result": task_result.result
        }
    elif task_result.state == "FAILED":
        return {"status": "failed"}
    else:
        return {"status": "pending"}
