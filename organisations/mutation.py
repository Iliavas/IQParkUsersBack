import graphene

from .gqlTypes import OrganisationType, RoleType, ChildType, TeacherType, GroupType, OrganisatorType
from .models import Organisation, Role, Group, Teacher, Child, Organisator
from lessons.models import SubjectClassLocal

from users.schema import UserType
from graphene import relay

from django.contrib.auth.models import User

from .mixins import RegModelToOrg, RegModelGroup, DeleteModelGroup

class CreateGroup(graphene.Mutation):
  class Arguments:
    org_name = graphene.String()
    groupName = graphene.String()
  
  group = graphene.Field(GroupType)

  def mutate(self, info, org_name, groupName, **kwargs):
    return CreateGroup(group=Group.objects.create(name=groupName, org=Organisation.objects.get(name=org_name)))


class CreateOrg(graphene.Mutation):
  class Arguments:
    name = graphene.String()
  
  Org = graphene.Field(OrganisationType)

  def mutate(self, info, name, **kwargs):
    return CreateOrg(Org=Organisation.objects.create(name=name))



class AddGroupToOrg(graphene.Mutation):
  class Arguments:
    orgName = graphene.String()
    groupName = graphene.String()
  
  group = graphene.Field(GroupType)
  def mutate(self, info, orgName, groupName):
    group = Group.objects.create(name=groupName, org=Organisation.objects.get(name=orgName))
    return AddGroupToOrg(group=group)



class RegTeacherToOrg(RegModelToOrg):
  model = Teacher
  modelType = graphene.Field(TeacherType)

class RegChildToOrg(RegModelToOrg):
  model = Child
  modelType =graphene.Field(ChildType)


class RegOrganisatorToOrg(RegModelToOrg):
  model = Organisator
  modelType = graphene.Field(OrganisatorType)


class RegChildGroup(RegModelGroup):
  model = Child
  modelType = graphene.Field(ChildType)


class DeleteChildGroup(DeleteModelGroup):
  model = Child
  modelType = graphene.Field(ChildType)


class DeleteGroup(graphene.Mutation):
  class Arguments:
    orgName = graphene.String()
    groupName = graphene.String()
  ok = graphene.Boolean()
  def mutate(self, info, orgName, groupName, **kwargs):
    Organisation.objects.find(name=orgName).objects.groups.all().filter(name=groupName)[0].delete()


class RegTeacherClass(graphene.Mutation):
  class Arguments:
    teacher_id = graphene.ID()
    class_id = graphene.ID()
  
  teacher = graphene.Field(TeacherType)

  def mutate(self, info, teacher_id, class_id):
    teacher = Teacher.objects.get(id=teacher_id)
    class_ = SubjectClassLocal.objects.get(id=class_id)

    class_.teachers.add(teacher)
    class_.save()
    return RegTeacherClass(teacher=teacher)


class DeleteTeacherClass(graphene.Mutation):
  class Arguments:
    teacher_id = graphene.ID()
    class_id = graphene.ID()

  teacher = graphene.Field(TeacherType)

  def mutate(self, info, teacher_id, class_id):
    class_ = SubjectClassLocal.objects.get(id=class_id)
    class_.teachers.filter(id=teacher_id)[0].remove()
    return DeleteTeacherClass(teacher=Teacher.objects.get(id=teacher_id))

class Mutation(graphene.ObjectType):
  create_org = CreateOrg.Field()
  create_group = CreateGroup.Field()
  add_group_to_org = AddGroupToOrg.Field()
  delete_group = DeleteGroup.Field()

  reg_teacher_org = RegTeacherToOrg.Field()
  reg_child_org = RegChildToOrg.Field()

  reg_child_group = RegChildGroup.Field()

  delete_child_group = DeleteChildGroup.Field()

  reg_teacher_class = RegTeacherClass.Field()
  delete_teacher_class = DeleteTeacherClass.Field()

  reg_organisator_to_org = RegOrganisatorToOrg.Field()