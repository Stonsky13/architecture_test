from __future__ import annotations
import os
from celery import Celery

BROKER_URL = os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@localhost:5672//")

celery_app = Celery("poc", broker=BROKER_URL, include=["app.tasks"])

celery_app.conf.update(
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_reject_on_worker_lost=True,
)
