import graphene
from .models import Organisation, Group
from django.contrib.auth.models import User

class RegModelToOrg(graphene.Mutation):
  model = ""
  
  class Arguments:
    user_id = graphene.ID()
    org_id = graphene.ID()
    name = graphene.String(required=False)
    surname = graphene.String(required=False)
    midname = graphene.String(required=False)
  modelType = graphene.Field(graphene.Int())


  @classmethod
  def mutate(self, root, info, **kwargs):
    surname = kwargs.get("surname", "")
    name = kwargs.get("name", "")
    midname = kwargs.get("midname", "")
    org_id = kwargs.get("org_id", "")
    user_id = kwargs.get("user_id", "")
    print(self.model, "model")
    profile = User.objects.get(id=user_id).profile
    print(kwargs, self)
    org = Organisation.objects.get(id=org_id)
    print(self, info)
    instance = self.model.objects.create(
      org=org, profile=profile, 
      name=name or "", surname=surname or "", midname = midname or "")
    return RegModelToOrg(modelType=instance)


class RegModelGroup(graphene.Mutation):
  model = ""
  modelType = graphene.Field(graphene.Int())
  class Arguments:
    group_id = graphene.ID()
    user_id = graphene.ID()
  

  @classmethod
  def mutate(self, root, info, group_id, user_id):
    group = Group.objects.get(id=group_id)
    user = self.model.objects.get(id=user_id)
    user.groups.add(group)
    user.save()
    return RegModelGroup(modelType=user)


class DeleteModelGroup(graphene.Mutation):
    model = ""
    modelType = graphene.Field(graphene.Int())

    class Arguments:
        group_id = graphene.ID()
        model_id = graphene.ID()


    @classmethod
    def mutate(self, root, info, group_id, model_id):
        model = self.model.objects.get(id=model_id)

        model.groups.all().filter(id=group_id)[0].delete()

        return DeleteModelGroup(modelType=model)
