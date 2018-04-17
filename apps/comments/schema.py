import graphene
from django.db.models import Q
from graphene_django import DjangoObjectType
from graphql import GraphQLError

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

    def mutate(self, info, post=None, content=None):
        user = info.context.user or None

        if user.is_anonymous:
            raise GraphQLError('You must be logged to comment!')

        if not post:
            raise GraphQLError('You don`t specify the post id!')

        if not content:
            raise GraphQLError('Comment shouldn`t be empty!')

        post_obj = Post.objects.filter(id=post).first()

        if not post_obj:
            raise Exception('Invalid Link!')

        comment = Comment.objects.create(post=post_obj,
                          content=content,
                          author=user)

        return CreateComment(
            id=comment.pk,
            post=post_obj,
            content=comment.content,
            author=comment.author,
        )


class Query(graphene.ObjectType):
    '''
    that`s the field that you can use on query top level
    '''

    comments = graphene.List(CommentType,
                             search=graphene.String(),
                             first=graphene.Int(),
                             skip=graphene.Int(),
                             )

    def resolve_comments(self, info, search=None, first=None, skip=None, **kwargs):
        qs = Comment.objects.all()

        if search:
            filter = Q(content__icontains=search)
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

    create_comment = CreateComment.Field()

