import graphene_django
from .models import Organisation, Role, Group, Teacher, Child, Organisator
from graphene import relay
import graphene

print(Teacher, Child)

class OrganisatorType(graphene_django.DjangoObjectType):
  class Meta:
    model = Organisator
    interfaces = (relay.Node,)
    filter_fields = {
      "name": ("exact", "contains"),
      "surname": ("exact", "contains"),
      "midname": ("exact", "contains"),
      "org" : ("exact",),
      "profile" : ("exact",),
      "groups" : ("contains",)
    }

class OrganisationType(graphene_django.DjangoObjectType):
  class Meta:
    model = Organisation
    interfaces = (relay.Node,)
    filter_fields = {
      "name" : ("exact", "contains",),
    }

class RoleType(graphene_django.DjangoObjectType):
  class Meta:
    model = Role


class TeacherType(graphene_django.DjangoObjectType):
  class Meta:
    model = Teacher
    interfaces = (relay.Node,)

    filter_fields = {
      "name": ("exact", "contains"),
      "surname": ("exact", "contains"),
      "midname": ("exact", "contains"),
      "org" : ("exact",),
      "profile" : ("exact",),
      "groups" : ("contains",)
    }
  pk = graphene.Int()

  def resolve_pk(self, info): return self.pk


class ChildType(graphene_django.DjangoObjectType):
  class Meta:
    model = Child

    interfaces = (relay.Node,)

    filter_fields = {
      "name": ("exact", "contains"),
      "surname": ("exact", "contains"),
      "midname": ("exact", "contains"),
      "org" : ("exact",),
      "profile" : ("exact",),
      "groups" : ("contains",)
    }
  pk = graphene.Int()

  def resolve_pk(self, info): return self.pk


class GroupType(graphene_django.DjangoObjectType):
  class Meta:
    model = Group
    interfaces = (relay.Node,)

    filter_fields = {
      "name" : ("exact", "contains"),
    }
  pk = graphene.Int()

  def resolve(self, info):
    return self.pk