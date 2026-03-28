from celery import Celery

task_queue = Celery("src")


def initialize_task_queue(host: str, port: int) -> None:
    global task_queue
    task_queue.conf.update(
        broker_url=f"redis://{host}:{port}/0",
        result_backend=f"redis://{host}:{port}/0",
        task_track_started=True,
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        worker_pool="solo",
        include=["src.tasks.model"],
    )
