import graphene
import graphene_django
from organisations.gqlTypes import TeacherType
from .models import HyperLink

from graphene import relay
from django.contrib.auth.models import User

class HyperLinkType(graphene_django.DjangoObjectType):
    class Meta:
        model = HyperLink



class getProfile(graphene.Mutation):
    class Arguments:
        profile_token = graphene.ID()
        user_id = graphene.ID()
    
    id = graphene.ID()
    user_type = graphene.String()

    def mutate(self, info, profile_token, user_id):
        user_type = ""
        user = User.objects.get(id=user_id)
        print(HyperLink.objects.all())
        hl = HyperLink.objects.get(link=profile_token)
        print(hl, "hl")
        model = hl.teacher or hl.child or hl.organ
        if hl.teacher: user_type = "teacher"
        if hl.child: user_type = "child"
        if hl.organ: user_type = "organ" 
        print(model, "profile")
        model.delete()
        model.profile = user.profile
        model.save()
        return getProfile(id=model.id, user_type = user_type)


class Mutation(graphene.ObjectType):
    get_profile = getProfile.Field()

class Query(graphene.ObjectType):
    hyper_links = graphene.Field(graphene.List(HyperLinkType))

    def resolve_hyper_links(self, info):
        return HyperLink.objects.all()



schema = graphene.Schema(query=Query, mutation=Mutation)