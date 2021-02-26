from django.db import models
from organisations.models import Organisation, Teacher, Group, Child

from django.dispatch import receiver
from django.db.models.signals import post_save


class Subject(models.Model):
  name = models.CharField(max_length=100)
  organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
  teachers_give = models.ManyToManyField(Teacher)

class SubjectClassLocal(models.Model):
  subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
  teachers = models.ManyToManyField(Teacher)
  group = models.ForeignKey(Group, on_delete=models.CASCADE)
  name = models.CharField(max_length=100, unique=False)

  def __str__(self):
    return self.name


class Lesson(models.Model):
  type_lesson = models.ForeignKey(SubjectClassLocal, on_delete=models.CASCADE)
  name = models.TextField(default="")
  descr = models.TextField(default="")
  content = models.TextField(default="")
  time_lesson = models.DateTimeField(auto_now=True)


class Materials(models.Model):
  link = models.URLField()
  name = models.CharField(max_length=100, blank=True)
  data = models.TextField(blank=True)
  Type = models.CharField(max_length=100, default="link")
  lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, default=3)


class Tests(models.Model):
  name = models.CharField(max_length=150)
  deadline = models.DateTimeField()
  lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
  is_timing = models.BooleanField(default=False)
  time_sec = models.IntegerField(default=300)

class Type(models.Model):
  name = models.TextField(max_length=150)


class TaskType(models.Model):
  name = models.TextField()


  def __str__(self) :
    return self.name

class Task(models.Model):
  theory = models.TextField()
  practise = models.TextField()
  test = models.ManyToManyField(Tests)
  types = models.ManyToManyField(Type)
  number = models.IntegerField()
  max_score = models.IntegerField(default=0)
  is_timing = models.BooleanField(default=False)
  time = models.IntegerField(default=30)
  Type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
  is_autoCheck = models.BooleanField(default=False)
  autoCheckData = models.TextField(blank=True)



  


class Theme(models.Model):
  tasks = models.ManyToManyField(Task)
  name = models.CharField(max_length=150)

class AnswerSheet(models.Model):
  child = models.ForeignKey(Child, on_delete=models.CASCADE)
  completed = models.BooleanField(default=False)
  test = models.ForeignKey(Tests, on_delete=models.CASCADE)

class Answer(models.Model):
  sheet = models.ForeignKey(AnswerSheet, on_delete=models.CASCADE)
  content = models.TextField()
  number = models.IntegerField()
  completed = models.BooleanField(default=False)
  score = models.IntegerField(default=0)