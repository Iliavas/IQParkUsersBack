import graphene

from .gqlTypes import OrganisationType, RoleType, GroupType
from .models import Organisation, Role, Group, Teacher, Child

from users.schema import UserType

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

class RegUserOrg(graphene.Mutation):
  class Arguments:
    token = graphene.String()
    orgName = graphene.String()
    isTeacher = graphene.Boolean()
    name = graphene.String(required=False)
    surname = graphene.String(required=False)
    midname = graphene.String(required=False)
  
  ok = graphene.Boolean()

  def mutate(self, info, token, orgName, isTeacher, **kwargs):
    org = Organisation.objects.get(name=orgName)
    if isTeacher:
      t = Teacher.objects.create(profile=info.context.user.profile, org=org)
    else:
      t = Child.objects.create(profile=info.context.user.profile, org=org)
    return RegUserOrg(ok=True)
      


class AddGroupToOrg(graphene.Mutation):
  class Arguments:
    orgName = graphene.String()
    groupName = graphene.String()
  
  group = graphene.Field(GroupType)
  def mutate(self, info, orgName, groupName):
    group = Group.objects.create(name=groupName, org=Organisation.objects.get(name=orgName))
    return AddGroupToOrg(group=group)


class RegUserGroup(graphene.Mutation):
  class Arguments:
    token = graphene.String()
    orgName = graphene.String()
    groupName = graphene.String()
    is_teacher = graphene.Boolean()
  user = graphene.Field(UserType)
  def mutate(self, info, token, orgName, groupName, is_teacher, **kwargs):
    group = Organisation.objects.get(name=orgName).group_set.all().filter(name=groupName)[0]
    if is_teacher:
      info.context.user.profile.teacher_set.all().filter(org__name=orgName)[0].groups.add(group)
    else:
      info.context.user.profile.child_set.all().filter(org__name=orgName)[0].groups.add(group)
    return RegUserGroup(info.context.user)

class DeleteGroup(graphene.Mutation):
  class Arguments:
    orgName = graphene.String()
    groupName = graphene.String()
  ok = graphene.Boolean()
  def mutate(self, info, orgName, groupName, **kwargs):
    Organisation.objects.find(name=orgName).objects.groups.all().filter(name=groupName)[0].delete()

class DeleteUserFromGroup(graphene.Mutation):
  class Arguments:
    orgName = graphene.String()
    groupName = graphene.String()
    token = graphene.String()
    is_teacher = graphene.Boolean()
  user = graphene.Field(UserType)
  def mutate(self, info, orgName, groupName, token, is_teacher, **kwargs):
    if is_teacher:
      group = info.context.user.profile.teacher_set.all().filter(org__name=orgName)[0].groups.all().filter(name=groupName)[0]
      org = info.context.user.profile.teacher_set.all().filter(org__name=orgName)[0]
      print(group, org)
      org.groups.remove(group)
      return DeleteuserFromGroup(info.context.user)
    else:
      group = info.context.user.profile.child_set.all().filter(org__name=orgName)[0].groups.all().filter(name=groupName)[0]
      org = info.context.user.profile.child_set.all().filter(org__name=orgName)[0]
      print(group, org)
      org.groups.remove(group)


class Mutation(graphene.ObjectType):
  create_org = CreateOrg.Field()
  reg_user_org = RegUserOrg.Field()
  create_group = CreateGroup.Field()
  reg_user_to_group = RegUserGroup.Field()
  add_group_to_org = AddGroupToOrg.Field()
  delete_group = DeleteGroup.Field()
  delete_user_from_group = DeleteUserFromGroup.Field()