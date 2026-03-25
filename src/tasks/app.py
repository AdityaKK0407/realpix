import os

from celery import Celery

host = os.getenv("REDIS_HOST")
port = os.getenv("REDIS_PORT")

if not host or not port:
    raise RuntimeError("REDIS_HOST and REDIS_PORT must be set")

task_queue: Celery = Celery(
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
