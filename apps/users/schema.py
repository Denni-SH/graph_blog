from django.contrib.auth import get_user_model
import graphene
from django.db.models import Q
from graphene_django import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    '''
    that`s the field that you can use on mutation top level
    '''
    create_user = CreateUser.Field()


class Query(graphene.ObjectType):
    '''
    that`s the field that you can use on query top level
    '''

    me = graphene.Field(UserType)
    users = graphene.List(UserType, search=graphene.String(), id=graphene.ID())

    def resolve_users(self, info, id=None, search=None):
        if id:
            filter = (
                Q(pk__iexact=id)
            )
            return get_user_model().objects.filter(filter)
        if search:
            filter = (
                Q(username__icontains=search)|
                Q(first_name__icontains=search)|
                Q(last_name__icontains=search)
            )
            return get_user_model().objects.filter(filter)

        return get_user_model().objects.all()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged!')

        return user

