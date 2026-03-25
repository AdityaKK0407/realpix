import time

from src.tasks.app import task_queue


@task_queue.task
def image_task(contents: tuple[bytes]) -> list[bool]:
    time.sleep(1)
    return [True] * len(contents)


@task_queue.task
def video_task(contents: tuple[bytes]) -> list[bool]:
    time.sleep(1)
    return [True] * len(contents)
