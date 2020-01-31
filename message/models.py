from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

from datetime import timedelta, datetime
import datetime

class Message(models.Model):
     sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
     receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
     msg_subject = models.CharField(max_length=50)
     msg_content = models.CharField(max_length=400)
     created_at = models.DateTimeField(default=(datetime.datetime.now() + timedelta(hours=1)), editable=False)
