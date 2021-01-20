import graphene

from .gqlTypes import OrganisationType, RoleType, TeacherType, ChildType, GroupType
from .models import Organisation, Role
from graphene import relay

from graphene_django.filter import DjangoFilterConnectionField

class Query(graphene.ObjectType):
  roles = graphene.Field(graphene.List(RoleType))

  organisations = DjangoFilterConnectionField(OrganisationType)
  organisation = relay.Node.Field(OrganisationType)

  teachers = DjangoFilterConnectionField(TeacherType)
  teacher = relay.Node.Field(TeacherType)

  children = DjangoFilterConnectionField(ChildType)
  child = relay.Node.Field(ChildType)

  group = relay.Node.Field(GroupType)
  groups = DjangoFilterConnectionField(GroupType)

  
  def resolve_roles(self, info, **kwargs):
    return Role.objects.all()