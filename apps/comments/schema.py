import graphene
from graphene_django import DjangoObjectType

from .models import Comment
from apps.users.schema import UserType
from apps.posts.models import Post
from apps.posts.schema import PostType

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment


class CreateComment(graphene.Mutation):
    id = graphene.Int()
    content = graphene.String()
    author = graphene.Field(UserType)
    post = graphene.Field(PostType)

    class Arguments:
        # need to be covered exceptions
        post = graphene.Int()
        content = graphene.String()

    def mutate(self, info, post, content):
        user = info.context.user or None

        if user.is_anonymous:
            raise Exception('You must be logged to vote!')

        cur_post = Post.objects.filter(id=post).first()
        if not cur_post:
            raise Exception('Invalid Link!')

        comment = Comment.objects.create(post=cur_post,
                          content=content,
                          author=user)

        return CreateComment(
            id=comment.pk,
            post=cur_post,
            content=comment.content,
            author=comment.author,
        )


class Query(graphene.ObjectType):
    comments = graphene.List(CommentType)

    def resolve_comments(self, info, **kwargs):
        return Comment.objects.all()


class Mutation(graphene.ObjectType):
    create_comment = CreateComment.Field()