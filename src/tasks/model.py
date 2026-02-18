import time

from src.tasks.app import task_queue


@task_queue.task
def image_task(filepath: str, content: bytes) -> dict[str, str | int]:
    time.sleep(10)
    return {"filepath": filepath, "content_size": len(content)}


# @task_queue.task
# def video_task(filepath: str, content: bytes) -> dict[str, str | int]:
#     time.sleep(10)
#     return {"filepath": filepath, "content_size": len(content)}
