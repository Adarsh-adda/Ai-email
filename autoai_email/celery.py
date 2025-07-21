import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoai_email.settings')

app = Celery('autoai_email')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
