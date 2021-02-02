from .models import Lesson
import graphene
import graphene_django
from graphene import relay
from .gqlTypes import TestsType


class LessonType(graphene_django.DjangoObjectType):
    class Meta:
        model=Lesson
        interfaces = (relay.Node,)
        filter_fields = {
            "name": ["exact", "contains"],
            "descr": ["exact", "contains"]
        }
    pk = graphene.Int()
    tests = graphene.List(TestsType)
    testsLen = graphene.Int()
    materialsLen = graphene.Int()
    materials = graphene.List(Material)

    def resolve_tests(self, info):
        return self.tests_set.all()

    def resolve_pk(self, info):
        return self.pk
    
    def resolve_testsLen(self, info):
        return len(self.tests_set.all())
    

    def resolve_materialsLen(self, info):
        return len(self.materials_set.all())
    

    def resolve_materials(self, info):
        return self.materials_set.all()