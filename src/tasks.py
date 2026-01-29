from src.celery_app import celery_app
import time

@celery_app.task
def long_running_task(x):
    time.sleep(10)
    return x ** 2