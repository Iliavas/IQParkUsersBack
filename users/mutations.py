import graphene

from django.contrib.auth.models import User

from .models import TimeEvent

from .graphqlTypes import UserType, TimeEventType

from graphql_relay.node.node import from_global_id

class CreateTimeEvent(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID()
        deadline = graphene.DateTime()
    
    ok = graphene.Boolean()
    

    @classmethod
    def mutate(cls, root, info, user_id, deadline):
        user_id = from_global_id(user_id)[1]
        user = User.objects.get(id=user_id)

        TimeEvent.objects.create(user = user, deadline = deadline)

        return CreateTimeEvent(ok=True)


class DeleteTimeEvent(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    

    ok = graphene.Boolean()


    @classmethod
    def mutate(cls, root, info, id):
        TimeEventId = from_global_id(id)[1]

        TimeEvent.objects.get(id=TimeEventId).delete()

        return DeleteTimeEvent(ok=True)


class ChangeTimeEventStatus(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        status = graphene.Boolean(required=False)
        deadline = graphene.DateTime(required = False)
    
    timeEvent = graphene.Field(TimeEventType)

    @classmethod
    def mutate(cls, root, info, id, status=None, deadline=None):
        TimeEventId = from_global_id(id)[1]
        print(TimeEventId, TimeEvent.objects.all())
        timeEvent = TimeEvent.objects.get(id=TimeEventId)
        print(timeEvent)
        timeEvent.deadline = deadline or timeEvent.deadline
        timeEvent.checked = status or timeEvent.checked

        timeEvent.save()

        return ChangeTimeEventStatus(timeEvent=timeEvent)

class RegUser(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        password = graphene.String()

    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, username, password):
        user = User.objects.create_user(username=username, password=password)

        return RegUser(user=user)