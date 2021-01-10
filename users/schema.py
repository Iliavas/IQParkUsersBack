import graphene
import graphql_jwt

import graphene_django

from django.contrib.auth.models import User

from .models import Profile

class UserType(graphene_django.DjangoObjectType):
  class Meta:
    model = User

class ProfileType(graphene_django.DjangoObjectType):
  class Meta:
    model = Profile

class RegisterUserInput(graphene.InputObjectType):
  username = graphene.String()
  password = graphene.String()

class RegisterUser(graphene.Mutation):
  class Arguments:
    input = RegisterUserInput(required=True)
  user = graphene.Field(UserType)

  def mutate(self, info, input=None):
    return RegisterUser(User.objects.create_user(username=input.username, password=input.password))

class Mutation(graphene.ObjectType):
  token_auth = graphql_jwt.ObtainJSONWebToken.Field()
  verify_token = graphql_jwt.Verify.Field()
  refresh_token = graphql_jwt.Refresh.Field()
  register_user = RegisterUser.Field()

class Query(graphene.ObjectType):
  hello = graphene.Field(graphene.String, token=graphene.String(required=True))
  user_info = graphene.Field(UserType, token=graphene.String(required=True))
  user_profile = graphene.Field(ProfileType, token=graphene.String(required=True))

  def resolve_hello(self, info, **kwargs):
    print(info.context.user.id)
    return "hello"

  def resolve_user_info(self, info, **kwargs):
    return info.context.user
  
  def resolve_user_profile(self, info, **kwargs):
    return info.context.user.profile

schema = graphene.Schema(query=Query, mutation=Mutation)