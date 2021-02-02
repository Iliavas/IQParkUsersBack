import graphene_django
from .models import Organisation, Role, Group, Teacher, Child, Organisator
from graphene import relay
import graphene


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
  children_length = graphene.Int()
  classes_length = graphene.Int()

  subjects = graphene.List(graphene.String)

  def resolve_children_length(self, info):
    print(self, self._meta.fields)
    return len(self.child_set.all())
  
  def resolve_classes_length(self, info):
    return len(self.group_set.all())
  
  def resolve_subjects(self, info):
    return list(map(lambda x : x.name, self.subject_set.all()))

class RoleType(graphene_django.DjangoObjectType):
  class Meta:
    model = Role




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

  def resolve_local_lessons(self, info):
    return self.subjectclasslocal_set.all()


from lessons.gqlTypes import LocalSubjectType

class GroupType(graphene_django.DjangoObjectType):
  class Meta:
    model = Group
    interfaces = (relay.Node,)

    filter_fields = {
      "name" : ("exact", "contains"),
    }
  pk = graphene.Int()
  classes = graphene.List(LocalSubjectType)
  childrenLen = graphene.Int()

  def resolve(self, info):
    return self.pk
  
  def resolve_classes(self, info):
    return self.subjectclasslocal_set.all()

  def resolve_childrenLen(self, info):
    return len(self.child_set.all())