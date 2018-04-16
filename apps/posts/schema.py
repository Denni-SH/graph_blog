import graphene
from graphene_django import DjangoObjectType

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

    def mutate(self, info, title, content):
        user = info.context.user or None
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
    posts = graphene.List(PostType)

    def resolve_posts(self, info, **kwargs):
        return Post.objects.all()


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()