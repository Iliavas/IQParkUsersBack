import graphene

class Query(graphene.ObjectType):
  hello = graphene.Field(graphene.String)

  def resolve_hello(self, info):
    return "hello"

schema = graphene.Schema(query=Query)