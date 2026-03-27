from celery import Celery

task_queue: Celery = Celery()


def initialize_task_queue(host: str, port: int) -> None:
    global task_queue
    task_queue = Celery(
        main="src",
        broker=f"redis://{host}:{port}/0",
        backend=f"redis://{host}:{port}/0",
        include=["src.tasks.model"],
    )

    task_queue.conf.update(
        task_track_started=True,
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        worker_pool="solo",
    )
