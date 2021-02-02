import graphene
import graphene_django

from .models import Subject, Lesson, SubjectClassLocal, Tests, Task, AnswerSheet, Answer, Materials
from organisations.gqlTypes import ChildType, TeacherType

from organisations.models import Organisation, Group, Child, Teacher

from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from users.models import Profile

from django.db.models import Model


class Material(graphene_django.DjangoObjectType):
    class Meta:
        model = Materials

class AnswerType(graphene_django.DjangoObjectType):
    class Meta:
        model = Answer
        interfaces = (relay.Node,)
        filter_fields = {
            "sheet" : ("exact",),
        }
    pk = graphene.Int()

    def resolve_pk(self, info): return self.pk

class AnswerSheetType(graphene_django.DjangoObjectType):
    class Meta:
        model = AnswerSheet
        interfaces = (relay.Node,)
        filter_fields = {
            "test" : ("exact",),
            "child": ("exact",)
        }


class TaskType(graphene_django.DjangoObjectType):
    class Meta:
        model = Task
        interfaces = (relay.Node,)
        filter_fields = {
            "test": ("exact",),
            "types": ("contains",)
        }
    pk = graphene.Int()

    def resolve_pk(self, info):
        return self.pk


class TestsType(graphene_django.DjangoObjectType):
    class Meta:
        model = Tests
        interfaces = (relay.Node,)
        filter_fields = {
            "name": ("exact", "contains"),
            "lesson": ("exact",)
        }
    pk = graphene.Int()
    taskLen = graphene.Int()

    def resolve_pk(self, info):
        return self.id
    

    def resolve_taskLen(self, info):
        return len(self.task_set.all())



class SubjectType(graphene_django.DjangoObjectType):
    class Meta:
        model=Subject
        interfaces = (relay.Node,)

        filter_fields = {
            "name" : ("exact", "contains",),
            "organisation" : ("exact",),
            "teachers_give" : ("contains",)
        }
    pk = graphene.Int()

    def resolve_pk(self, info): return self.pk


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


class LocalSubjectType(graphene_django.DjangoObjectType):
    class Meta:
        model=SubjectClassLocal
        interfaces = (relay.Node,)
        filter_fields = {
            "name": ("exact", "contains"),
            "id": ("exact",),
            "group": ("exact",)
        }
    pk = graphene.Int()
    teachers_set = graphene.List(TeacherType)
    lessonsLen = graphene.Int()

    def resolve_pk(self, info):
        return self.pk
    

    def resolve_teachers_set(self, info):
        return self.teachers.all()
    

    def resolve_lessonsLen(self, info):
        return len(self.lesson_set.all())


