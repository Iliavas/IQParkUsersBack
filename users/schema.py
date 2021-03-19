import graphene

from graphene_django import DjangoObjectType

from .graphqlTypes import DisposableEventType, UserType, TimeEventType, StaffEventType
from graphene_django.filter import DjangoFilterConnectionField

from .mutations import *

import graphql_jwt

class Query(graphene.ObjectType):
    DisposableEvents = DjangoFilterConnectionField(DisposableEventType)
    DisposableEvent = graphene.relay.Node.Field(DisposableEventType)


    TimeEvents = DjangoFilterConnectionField(TimeEventType)
    TimeEvent = graphene.relay.Node.Field(TimeEventType)


    StaffEvents = DjangoFilterConnectionField(StaffEventType)
    StaffEvent = graphene.relay.Node.Field(StaffEventType)


    Users = DjangoFilterConnectionField(UserType)
    User = graphene.relay.Node.Field(UserType)


class Mutation(graphene.ObjectType):
    createTimeEvent = CreateTimeEvent.Field()
    deleteTimeEvent = DeleteTimeEvent.Field()
    changeTimeEventStatus = ChangeTimeEventStatus.Field()

    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    registration = RegUser.Field()
