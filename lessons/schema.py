import graphene
import graphene_django

from .models import Subject, Lesson, SubjectClassLocal, Tests, Task, AnswerSheet, Answer
from organisations.gqlTypes import ChildType, TeacherType

from organisations.models import Organisation, Group, Child, Teacher

from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from users.models import Profile

from django.db.models import Model


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

    def resolve_pk(self, info):
        return self.id



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

    def resolve(self, info):
        return self.pk
        

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

    def resolve_pk(self, info):
        return self.pk

class CreateLesson(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        descr = graphene.String()
        subject = graphene.ID()
    
    ok = graphene.Boolean()

    def mutate(self, info, name, descr, subject):
        Lesson.objects.create(name=name, descr=descr, type_lesson=
            SubjectClassLocal.objects.get(pk=subject))
        return CreateLesson(ok=True)

class UpdateLessonRegistration(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        descr = graphene.String()
        name = graphene.String()
    ok = graphene.Boolean()

    def mutate(self, info, id, descr=None, name=None):
        lesson = Lesson.objects.get(id=id) or None
        if lesson == None: return UpdateLessonRegistration(ok=False)
        descr_upd = lesson.descr
        name_upd = lesson.name
        if descr != None: descr_upd = descr
        if name != None: name_upd = name
        lesson.descr = descr_upd
        lesson.name = name_upd
        lesson.save()
        return UpdateLessonRegistration(ok=True)


class DeleteLesson(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    ok = graphene.Boolean()

    def mutate(self, info, id):
        lesson = Lesson.objects.get(id=id)
        if lesson == None: return DeleteLesson(ok=False)
        lesson.delete()
        return DeleteLesson(ok=True)

import datetime #fix
class CreateTest(graphene.Mutation):
    class Arguments:
        lesson_id = graphene.ID()
        name = graphene.String()
        deadline = graphene.Date()
    
    test = graphene.Field(TestsType)

    def mutate(self, info, lesson_id, name, deadline=None):
        lesson = Lesson.objects.get(id=lesson_id)
        t = Tests.objects.create(name=name, lesson=lesson, deadline=datetime.datetime.now())
        return CreateTest(test=t)

class updateTestRegistration(graphene.Mutation):
    class Arguments:
        test_id = graphene.ID()
        name = graphene.String()
        deadline = graphene.Date()
    test = graphene.Field(TestsType)

    def mutate(self, info, test_id, name=None, deadline=None):
        test = Tests.objects.get(id=test_id)
        name_changed = test.name
        deadline_changed = test.deadline
        if name != None: name_changed = name
        if deadline != None : deadline_changed = deadline
        test.name = name_changed
        test.deadline = deadline_changed
        return updateTestRegistration(test)
from collections.abc import Mapping

class deleteTest(graphene.Mutation):
    class Arguments:
        test_id = graphene.ID()
    ok = graphene.Boolean()

    def mutate(self, info, test_id):
        test = Tests.objects.get(id=test_id)
        test.delete()
        return deleteTest(ok=True)


def createModel(model, fields):
    return model.objects.create(**fields)

def updateModel(model:Model, instance:Model, fields:Mapping):
    print(fields)
    updated_fields = {}
    for key, value in fields.items():
        updated_fields.update({key: value[0] or value[1]})
    print(updated_fields)
    for key, value in updated_fields.items():
        setattr(instance, key, value)
    instance.save()
    return instance

def deleteModel(model:Model):
    model.delete()
    

class createTask(graphene.Mutation):
    class Arguments:
        test_id = graphene.ID()
        theory = graphene.String()
        practise = graphene.String()
        number = graphene.Int()
        max_score = graphene.Int()
    
    task = graphene.Field(TaskType)

    def mutate(self, info, test_id, theory, practise, number, max_score):
        m = createModel(model=Task, fields = {
            "test": Tests.objects.get(id=test_id),
            "theory": theory,
            "practise": practise,
            "number": number,
            "max_score": max_score
            })
        return createTask(task=m)

class updateTask(graphene.Mutation):
    class Arguments:
        task_id = graphene.ID()
        theory = graphene.String()
        practise = graphene.String()
        number = graphene.Int()
        max_score = graphene.Int()
    task = graphene.Field(TaskType)

    def mutate(self, info, task_id, theory=None, practise=None, number=None, max_score=None):
        task = Task.objects.get(id=task_id)
        m = updateModel(Task, task, {
            "theory": [theory, task.theory],
            "practise": [practise, task.practise],
            "number": [number, task.number],
            "max_score": [max_score, task.max_score]
        })
        return updateTask(task=m)


class deleteTask(graphene.Mutation):
    class Arguments:
        task_id = graphene.ID()
    
    ok = graphene.Boolean()
    def mutate(self, info, task_id):
        deleteModel(Task.objects.get(id=task_id))
        return deleteTask(ok=True)

class addChildToGroup(graphene.Mutation):
    class Arguments:
        group_id = graphene.ID()
        child_id = graphene.ID()
    
    child = graphene.Field(ChildType)

    def mutate(self, info, group_id, child_id):
        group = Group.objects.get(id=group_id)
        child = Child.objects.get(id=child_id)
        child.groups.add(group)
        child.save()
        return addChildToGroup(child=child)

class addChildToOrg(graphene.Mutation):
    class Arguments:
        org_id = graphene.ID()
        child_id = graphene.ID()
        name = graphene.String()
        surname = graphene.String()
        midname = graphene.String()

    child = graphene.Field(ChildType)

    def mutate(self, info, org_id, child_id, name, surname, midname):
        user = Profile.objects.get(id=child_id)
        org = Organisation.objects.get(id=org_id)

        child = Child.objects.create(profile=user, org=org, name=name or "",
            surname = surname or "", midname = midname or "")
        return addChildToOrg(child=child) 

class CreateSubjectClass(graphene.Mutation):
    class Arguments:
        group_id = graphene.ID()
        subject_id = graphene.ID()
        name = graphene.String()
    
    subject_class = graphene.Field(LocalSubjectType)

    def mutate(self, info, group_id, subject_id, name):
        group = Group.objects.get(id=group_id)
        subject = Subject.objects.get(id=subject_id)
        local_subject = SubjectClassLocal.objects.create(name=name,
        group=group, subject=subject)
        return CreateSubjectClass(subject_class=local_subject)


class CreateSubject(graphene.Mutation):
    class Arguments:
        org_id = graphene.ID()
        name = graphene.String()
    
    subject = graphene.Field(SubjectType)

    def mutate(self, info, org_id, name):
        org = Organisation.objects.get(id=org_id)
        subject = Subject.objects.create(name=name, organisation=org)
        return CreateSubject(subject)

class UpdateSubjectReg(graphene.Mutation):
    class Arguments:
        subject_id = graphene.ID()
        name = graphene.String()
    
    subject = graphene.Field(SubjectType)

    def mutate(self, info, subject_id, name):
        subject = Subject.objects.get(id=subject_id)
        subject.name = name or subject.name
        subject.save()
        return UpdateSubjectReg(subject=subject)

class DeleteSubject(graphene.Mutation):
    class Arguments:
        subject_id = graphene.ID()
    
    ok = graphene.Boolean()

    def mutate(self, info, subject_id):
        subject = Subject.objects.get(id=subject_id)
        subject.delete()
        return DeleteSubject(ok=True)


class UpdateSubjectLocalReg(graphene.Mutation):
    class Arguments:
        subject_local_id = graphene.ID()
        name = graphene.String()
    
    subject_local = graphene.Field(LocalSubjectType)

    def mutate(self, info, subject_local_id, name):
        subject = SubjectClassLocal.objects.get(id=subject_local_id)
        subject.name = name or subject.name
        subject.save()
        return UpdateSubjectLocalReg(subject_local=subject)


class DeleteSubjectLocal(graphene.Mutation):
    class Arguments:
        subject_local_id = graphene.ID()
    
    ok = graphene.Boolean()

    def mutate(self, info, subject_local_id):
        SubjectClassLocal.objects.get(id=subject_local_id).delete()
        return DeleteSubjectLocal(ok=True)


class AddSubjectToTeacher(graphene.Mutation):
    class Arguments:
        subject_id = graphene.ID()
        teacher_id = graphene.ID()
    teacher = graphene.Field(TeacherType)

    def mutate(self, info, subject_id, teacher_id):
        teacher = Teacher.objects.get(id=teacher_id)
        subject= Subject.objects.get(id=subject_id)

        subject.teachers_give.add(teacher)
        subject.save()
        return AddSubjectToTeacher(teacher=teacher)


class RemoveSubjectFromTeacher(graphene.Mutation):
    class Arguments:
        subject_id = graphene.ID()
        teacher_id = graphene.ID()
    teacher = graphene.Field(TeacherType)

    def mutate(self, info, subject_id, teacher_id):
        subject = Subject.objects.get(id=subject_id)
        subject.teachers_give.all().filter(id=teacher_id)[0].delete()
        return RemoveSubjectFromTeacher(teacher=Teacher.objects.get(id=teacher_id))


class AnswerQuestion(graphene.Mutation):
    class Arguments:
        answer_table_id = graphene.ID()
        answer = graphene.String()
    
    answer = graphene.Field(AnswerType)

    def mutate(self, info, answer_table_id, answer):
        answerT = Answer.objects.get(id=answer_table_id)
        answerT.content = answer
        answerT.completed = True
        answerT.save()
        return AnswerQuestion(answer=answerT)


class Mutation(graphene.ObjectType):
    create_lesson = CreateLesson.Field()
    update_lesson_registration = UpdateLessonRegistration.Field()
    delete_lesson = DeleteLesson.Field()

    create_test = CreateTest.Field()
    update_test_registration = updateTestRegistration.Field()
    delete_test = deleteTest.Field()

    create_task = createTask.Field()
    update_task = updateTask.Field()
    delete_task = deleteTask.Field()

    add_child_to_group = addChildToGroup.Field()
    add_child_to_org = addChildToOrg.Field()

    create_subject_class = CreateSubjectClass.Field()
    update_subject_class = UpdateSubjectLocalReg.Field()
    delete_subject_class = DeleteSubjectLocal.Field()

    create_subject = CreateSubject.Field()
    update_subject = UpdateSubjectReg.Field()
    delete_subject = DeleteSubject.Field()

    add_subject_to_teacher = AddSubjectToTeacher.Field()
    remove_subject_from_teacher = RemoveSubjectFromTeacher.Field()

    answer_question = AnswerQuestion.Field()

class Query(graphene.ObjectType):

    all_test = DjangoFilterConnectionField(TestsType)
    test = relay.Node.Field(TestsType)

    all_subject = DjangoFilterConnectionField(SubjectType)
    subject = relay.Node.Field(SubjectType)

    task = relay.Node.Field(TaskType)
    all_task = DjangoFilterConnectionField(TaskType)

    answer_sheet = relay.Node.Field(AnswerSheetType)
    all_answer_sheet = DjangoFilterConnectionField(AnswerSheetType)

    answer = relay.Node.Field(AnswerType)
    all_answer = DjangoFilterConnectionField(AnswerType)

    all_lessons = DjangoFilterConnectionField(LessonType)
    lessons = relay.Node.Field(LessonType)

    subject_class = relay.Node.Field(LocalSubjectType)
    subject_classes = DjangoFilterConnectionField(LocalSubjectType)

schema = graphene.Schema(query=Query)