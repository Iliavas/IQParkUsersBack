import graphene_django
from .models import Organisation, Role, Group, Teacher, Child

print(Teacher, Child)

class OrganisationType(graphene_django.DjangoObjectType):
  class Meta:
    model = Organisation

class RoleType(graphene_django.DjangoObjectType):
  class Meta:
    model = Role


class GroupType(graphene_django.DjangoObjectType):
  class Meta:
    model = Group


class TeacherType(graphene_django.DjangoObjectType):
  class Meta:
    model = Teacher


class ChildType(graphene_django.DjangoObjectType):
  class Meta:
    model = Child