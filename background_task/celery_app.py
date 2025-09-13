from celery import Celery

celery_app = Celery(
    "background_task",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["background_task.example_tasks"],  # tasks
)

celery_app.conf.update(
    timezone="UTC",
    task_track_started=True,
    result_expires=3600,
)

# ✅ Import beat_schedule after creating celery_app
from . import beat_schedule
