from celery import Celery

from app.core.config import get_settings
from app.infra.redis_broker import get_broker_url

settings = get_settings()
broker_url = get_broker_url(settings)

celery_app = Celery(
    "survey_pal",
    broker=broker_url,
    backend=broker_url,
    include=[],
)
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Shanghai",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    broker_connection_retry_on_startup=True,
)
