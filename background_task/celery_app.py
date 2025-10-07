from celery import Celery
from fastapi_mail import ConnectionConfig


celery_app = Celery(
    "background_task",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["background_task.example_tasks"],  # tasks
)

mail_conf = ConnectionConfig(
    MAIL_USERNAME="priyanhari2303@gmail.com",
    MAIL_PASSWORD="frms xadf rhqh sing",
    MAIL_FROM="priyanhari2303@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

celery_app.conf.update(
    timezone="UTC",
    task_track_started=True,
    result_expires=3600,
)

# ✅ Import beat_schedule after creating celery_app
# from . import beat_schedule
