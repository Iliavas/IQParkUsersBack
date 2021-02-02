from django.db import models

from organisations.models import Organisator, Child, Teacher

import uuid

from django.dispatch import receiver
from django.db.models.signals import post_save

class HyperLink(models.Model):
    link = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=False)
    teacher = models.OneToOneField(Teacher, null=True, on_delete=models.CASCADE, unique=False)
    child = models.OneToOneField(Child, null=True, on_delete=models.CASCADE, unique=False)
    organ = models.OneToOneField(Organisator, null=True, on_delete=models.CASCADE, unique=False)

#@receiver(signal=post_save, sender=Organisator)
#def org_recieve(sender, instance, **kwargs):
#    HyperLink.objects.create(organ=instance)



@receiver(signal=post_save, sender=Child)
def child_recieve(sender, instance, **kwargs):
    HyperLink.objects.create(child=instance)



@receiver(signal=post_save, sender=Teacher)
def teacher_recieve(sender, instance, **kwargs):
    HyperLink.objects.create(teacher=instance)
