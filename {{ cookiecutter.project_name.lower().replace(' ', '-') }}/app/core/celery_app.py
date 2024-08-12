from celery import Celery
from app.config.config import settings
from celery.schedules import crontab

celery_app = Celery(
    "worker",
    broker=settings.celery.broker_url,
    backend=settings.celery.result_backend,
    include=["app.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

celery_app.conf.task_routes = {
    "app.tasks.*": {"queue": "default"}
}

celery_app.conf.task_default_queue = "default"

celery_app.conf.task_annotations = {
    '*': {
        'rate_limit': '10/s'
    }
}

celery_app.conf.task_queues = {
    "default": {
        "exchange": "default",
        "routing_key": "default",
    },
    "high-priority": {
        "exchange": "high-priority",
        "routing_key": "high-priority",
    },
    "low-priority": {
        "exchange": "low-priority",
        "routing_key": "low-priority",
    }
}
# celery -A app.core.celery_app worker --loglevel=info

# Планировщик задач celery
celery_app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'app.tasks.example_task',
        'schedule': 30.0,
        'args': (16, 16)
    },
    'important-daily-task': {
        'task': 'app.tasks.important_task',
        'schedule': crontab(hour=0, minute=0),  # каждый день в полночь
    },
}
# celery -A app.core.celery_app beat --loglevel=info


@celery_app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@celery_app.task(queue="high-priority")
def important_task():
    pass

# Пример использования:
# @app.post("/important-action")
# async def important_action():
#     task = important_task.delay()
#     return {"task_id": task.id}
#
# @app.get("/task/{task_id}")
# async def get_task_result(task_id: str):
#     task = celery_app.AsyncResult(task_id)
#     if task.ready():
#         return {"status": "completed", "result": task.result}
#     return {"status": "pending"}
