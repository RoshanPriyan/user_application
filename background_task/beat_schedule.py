from datetime import timedelta
from .celery_app import celery_app

celery_app.conf.beat_schedule = {
    "print-message-every-10s": {
        "task": "background_task.example_tasks.print_message",
        "schedule": timedelta(seconds=10),
        "args": ("Hello from Celery Beat",),
    },
}
