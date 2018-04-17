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

    posts = graphene.List(PostType, search=graphene.String(), id=graphene.ID())

    def resolve_posts(self, info, id=None, search=None, **kwargs):
        if id:
            filter = (
                Q(pk__iexact=id)
            )
            return Post.objects.filter(filter)
        if search:
            filter = (
                Q(title__icontains=search) |
                Q(content__icontains=search)
            )
            return Post.objects.filter(filter)
        return Post.objects.all()


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()