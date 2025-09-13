from .celery_app import celery_app

@celery_app.task
def print_message(msg: str):
    print(f"Message from task: {msg}")
    return f"Processed: {msg}"
