import graphene

from .gqlTypes import OrganisationType, RoleType
from .models import Organisation, Role


class Query(graphene.ObjectType):
  organisations = graphene.Field(graphene.List(OrganisationType))
  roles = graphene.Field(graphene.List(RoleType))

  def resolve_organisations(self, info, **kwargs):
    return Organisation.objects.all()
  
  def resolve_roles(self, info, **kwargs):
    return Role.objects.all()