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


class Materials(models.Model):
  link = models.URLField()
  name = models.CharField(max_length=100, blank=True)


class Tests(models.Model):
  name = models.CharField(max_length=150)
  deadline = models.DateTimeField()
  lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

class Type(models.Model):
  name = models.TextField(max_length=150)

class Task(models.Model):
  theory = models.TextField()
  practise = models.TextField()
  test = models.ForeignKey(Tests, on_delete=models.CASCADE)
  type = models.ForeignKey(Type, on_delete=models.PROTECT)
  number = models.IntegerField()



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


@receiver(post_save, sender=Tests)
def _post_save_receiver(sender, instance, created, **kwargs):
  if created:
    for child in instance.lesson.type_lesson.group.child_set.all():
      AnswerSheet.objects.create(child=child, completed=False, test=instance)

@receiver(post_save, sender=Task)
def _post_save_receiver(sender, instance, created, **kwargs):
  if created:
    for child in instance.test.lesson.type_lesson.group.child_set.all():
      Answer.objects.create(number=instance.number, sheet=child.answer_sheet_set.all().filter(test=instance.test)[0], content="")