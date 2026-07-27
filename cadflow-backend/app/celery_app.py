from app.core.config import settings
from celery import Celery

celery_app = Celery(
    "cadflow_tasks",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=['app.tasks']
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)
