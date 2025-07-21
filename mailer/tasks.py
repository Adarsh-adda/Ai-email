from celery import shared_task
from .utils import fetch_and_reply_emails

@shared_task
def check_and_reply_task():
    fetch_and_reply_emails()