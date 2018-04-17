import graphene
from graphene_django import DjangoObjectType

from .models import Post
from apps.users.schema import UserType
from apps.comments.models import Comment

class PostType(DjangoObjectType):
    class Meta:
        model = Post


class CreatePost(graphene.Mutation):
    import apps.comments.schema

    id = graphene.Int()
    title = graphene.String()
    content = graphene.String()
    author = graphene.Field(UserType)
    # comments = graphene.Field(apps.comments.schema.CommentType)

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
            # author=post.author,
            # comments=None
        )


class Query(graphene.ObjectType):
    import apps.comments.schema

    posts = graphene.List(PostType)
    comments = graphene.List(apps.comments.schema.CommentType)

    def resolve_posts(self, info, **kwargs):
        return Post.objects.all()

    def resolve_comments(self, info, **kwargs):
        return Comment.objects.all()


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()