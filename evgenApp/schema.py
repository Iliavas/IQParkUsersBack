import graphene
import users.schema
import organisations.schema
import lessons.schema
import hyperlinks.schema

class Query(users.schema.Query, organisations.schema.Query, 
              lessons.schema.Query, hyperlinks.schema.Query, graphene.ObjectType):
  pass

class Mutation(users.schema.Mutation, organisations.schema.Mutation, 
              lessons.schema.Mutation, hyperlinks.schema.Mutation, graphene.ObjectType):
  pass


schema = graphene.Schema(query=Query, mutation=Mutation)