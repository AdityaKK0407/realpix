from celery import Celery

task_queue: Celery = Celery(
    main="src",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["src.tasks.model"],
)

task_queue.conf.update(
    task_track_started=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    worker_pool="solo",
)
