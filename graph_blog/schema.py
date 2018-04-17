import graphene

from apps.posts.schema import (Query as PostQuery,
                               Mutation as PostMutation)
from apps.users.schema import (Mutation as UserMutation,
                               Query as UserQuery)
import graphql_jwt

from apps.comments.schema import (Mutation as CommentMutation,
                                  Query as CommentQuery)


# ===============================================================================
# All general schemas
class Query(UserQuery, PostQuery, CommentQuery, graphene.ObjectType):
    pass


class Mutation(UserMutation, PostMutation, CommentMutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
# ===============================================================================
