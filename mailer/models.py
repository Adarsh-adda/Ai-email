# Create your models here.
from django.db import models

class EmailLog(models.Model):
    sender = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    reply = models.TextField(blank=True, null=True)
    replied = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)