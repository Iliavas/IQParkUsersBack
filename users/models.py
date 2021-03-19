from django.db import models

from django.contrib.auth.models import User


class Profile(models.Model):
    pass


class Event(models.Model):
    class Meta:
        abstract = True
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    checked = models.BooleanField(default=True)
    deadline = models.DateTimeField()


class DisposableEvent(Event):

    used = models.BooleanField()


class TimeEvent(Event): pass


class StaffEvent(Event):
    timeTable = models.TextField()