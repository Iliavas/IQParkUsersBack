import graphene

from graphene_django import DjangoObjectType

from django.contrib.auth.models import User

from .models import DisposableEvent, TimeEvent, StaffEvent



class DisposableEventType(DjangoObjectType):
    class Meta:
        model = DisposableEvent
        interfaces = [graphene.relay.Node]

        filter_fields = {
            "user__id": ["exact"]
        }

class UserType(DjangoObjectType):
    class Meta:
        model = User 

        interfaces = [graphene.relay.Node]

        filter_fields = ["username"]


class TimeEventType(DjangoObjectType):
    class Meta:
        model = TimeEvent

        interfaces = [graphene.relay.Node]

        filter_fields = {
            "user__id" : ["exact"]
        }


class StaffEventType(DjangoObjectType):
    class Meta:
        model = StaffEvent

        interfaces = [graphene.relay.Node]

        filter_fields = {
            "user__id": ["exact"]
        }