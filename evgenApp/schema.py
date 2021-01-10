import graphene
import users.schema
import organisations.schema

class Query(users.schema.Query, organisations.schema.Query, graphene.ObjectType):
  pass

class Mutation(users.schema.Mutation, organisations.schema.Mutation, graphene.ObjectType):
  pass


schema = graphene.Schema(query=Query, mutation=Mutation)