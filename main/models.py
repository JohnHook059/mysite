from django.db import models
from django.utils.timezone import now
from django.conf import settings

class Message(models.Model):
    inp = models.CharField(max_length=100)
    outp = models.CharField(max_length=100)
    text = models.CharField(max_length=1000000)
    time = models.DateTimeField(default=now)

    class Meta:
        ordering = ['-time']

class Invite(models.Model):
    author = models.CharField(max_length=100)
    is_used = models.BooleanField(default=False)
    owner = models.CharField(max_length=100)
    invite = models.CharField(max_length=100)
    time = models.DateTimeField(default=now)

    class Meta:
        ordering = ['-time']
