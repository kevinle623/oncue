from celery import Celery  # type: ignore[import-untyped]

from oncue.settings import settings

celery_app = Celery(
    "oncue",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["oncue.workers.tasks"],
)
