from fastapi_mail import FastMail, MessageSchema
from .celery_app import celery_app, mail_conf
import asyncio


@celery_app.task
def print_message(msg: str):
    print(f"Message from task: {msg}")
    return f"Processed: {msg}"


@celery_app.task(bind=True, max_retries=3)
def send_verification_email(self, email: str, token: str):
    """Send email with verification link"""
    verification_link = f"https://yourapp.com/verify?token={token}"

    html = f"""
    <h3>Welcome to SpiceGhats!</h3>
    <p>Click below to verify your email:</p>
    <a href="{verification_link}" 
       style="background:#8B0000;color:#fff;padding:10px 20px;text-decoration:none;border-radius:5px;">
       Verify My Email</a>
    """

    message = MessageSchema(
        subject="Verify your email - SpiceGhats",
        recipients=[email],
        body=html,
        subtype="html"
    )

    try:
        fm = FastMail(mail_conf)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(fm.send_message(message))
    except Exception as exc:
        raise self.retry(exc=exc, countdown=10)  # retry after 10s if failed
