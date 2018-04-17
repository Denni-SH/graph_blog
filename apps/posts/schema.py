import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q
from graphql import GraphQLError

from .models import Post
from apps.users.schema import UserType


class PostType(DjangoObjectType):
    class Meta:
        model = Post


class CreatePost(graphene.Mutation):

    id = graphene.Int()
    title = graphene.String()
    content = graphene.String()
    author = graphene.Field(UserType)

    class Arguments:
        title = graphene.String()
        content = graphene.String()

    def mutate(self, info, title=None, content=None, **kwargs):
        user = info.context.user or None

        if not title and not content:
            raise GraphQLError('You must be forget to provide post title and content!')
        elif not title:
            raise GraphQLError('You must be forget to provide post title!')
        elif not content:
            raise GraphQLError('Post content shouldn`t be empty!')

        post = Post(title=title,
                    content=content,
                    author=user)
        post.save()

        return CreatePost(
            id=post.pk,
            title=post.title,
            content=post.content,
            author=post.author,
        )


class Query(graphene.ObjectType):
    '''
    that`s the field that you can use on query top level
    '''

    posts = graphene.List(PostType,
                          search=graphene.String(),
                          id=graphene.ID(),
                          first=graphene.Int(),
                          skip=graphene.Int(),
                          )

    def resolve_posts(self, info, id=None, search=None, first=None, skip=None, **kwargs):
        qs = Post.objects.all()

        if id:
            filter = (
                Q(pk__iexact=id)
            )
            qs = qs.filter(filter)

        if search:
            filter = (
                Q(title__icontains=search) |
                Q(content__icontains=search)
            )
            qs = qs.filter(filter)

        if skip:
            qs = qs[skip::]

        if first:
            qs = qs[:first]

        return qs


class Mutation(graphene.ObjectType):
    '''
    that`s the field that you can use on mutation top level
    '''

    create_post = CreatePost.Field()

