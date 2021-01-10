import graphene_django
import graphene


from .mutation import Mutation

from .query import Query

schema = graphene.Schema(query=Query, mutation=Mutation)