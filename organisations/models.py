from django.db import models


from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Profile

class Role(models.Model):
  name = models.CharField(max_length=50)



class Organisation(models.Model):
  name = models.TextField()

  def __str__(self):
    return self.name


class Group(models.Model):
  name = models.CharField(max_length=20)
  org = models.ForeignKey(Organisation, models.CASCADE, unique=False)

  def __str__(self):
    return self.name


class Teacher(models.Model):
  org = models.ForeignKey(Organisation, models.CASCADE, blank=True)
  profile = models.ForeignKey(Profile, models.CASCADE)
  groups = models.ManyToManyField(Group)
  name = models.CharField(max_length=150, blank=True)
  surname = models.CharField(max_length=150, blank=True)
  midname = models.CharField(max_length=150, blank=True)

class Child(models.Model):
  profile = models.ForeignKey(Profile, models.CASCADE)
  org = models.ForeignKey(Organisation, models.CASCADE, blank=True)
  groups = models.ManyToManyField(Group)
  name = models.CharField(max_length=150, blank=True)
  surname = models.CharField(max_length=150, blank=True)
  midname = models.CharField(max_length=150, blank=True)