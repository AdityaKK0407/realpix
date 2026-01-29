from celery import Celery

celery_app: Celery = Celery(
    main="src",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["src.tasks"]
)

celery_app.conf.update(
    task_track_started=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    worker_pool="solo"
)