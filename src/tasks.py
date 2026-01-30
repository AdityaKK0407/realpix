from src.celery_app import task_queue
import time

@task_queue.task
def image_task(filepath: str, content: bytes):
    time.sleep(10)
    return {
        "filepath": filepath,
        "content-size": len(content)
    }

@task_queue.task
def video_task(filepath: str, content: bytes):
    time.sleep(10)
    return {
        "filepath": filepath,
        "content-size": len(content)
    }