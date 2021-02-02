import graphene
import graphql_jwt

import graphene_django

from django.contrib.auth.models import User

from .models import Profile

from graphene import relay

from graphene_django.filter import DjangoFilterConnectionField

class UserType(graphene_django.DjangoObjectType):
  class Meta:
    model = User
  pk = graphene.Int()

  def resolve_pk(self, info):
    return self.pk

class ProfileType(graphene_django.DjangoObjectType):
  class Meta:
    model = Profile
    interfaces = (relay.Node,)
    filter_fields = {
      "user__username" : ("exact","contains")
    }
  pk = graphene.Int()

  def resolve_pk(self, info):
    return self.pk

class RegisterUserInput(graphene.InputObjectType):
  username = graphene.String()
  password = graphene.String()

class RegisterUser(graphene.Mutation):
  class Arguments:
    input = RegisterUserInput(required=True)
  ok = graphene.Boolean()

  def mutate(self, info, input=None):
    try:
      User.objects.create_user(username=input.username, password=input.password)
    except:
      return RegisterUser(ok=False)
    return RegisterUser(ok=True)

class Mutation(graphene.ObjectType):
  token_auth = graphql_jwt.ObtainJSONWebToken.Field()
  verify_token = graphql_jwt.Verify.Field()
  refresh_token = graphql_jwt.Refresh.Field()
  register_user = RegisterUser.Field()

class Query(graphene.ObjectType):
  hello = graphene.Field(graphene.String, token=graphene.String(required=True))
  user_info = graphene.Field(UserType, token=graphene.String(required=True))
  profile = relay.Node.Field(ProfileType)
  all_profiles = DjangoFilterConnectionField(ProfileType)

  def resolve_hello(self, info, **kwargs):
    print(info.context.user.id)
    return "hello"

  def resolve_user_info(self, info, **kwargs):
    return info.context.user

schema = graphene.Schema(query=Query, mutation=Mutation)