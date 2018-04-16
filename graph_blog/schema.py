import graphene

from apps.posts.schema import (Query as PostQuery,
                               Mutation as PostMutation)
from apps.users.schema import (Mutation as UsersMutation,
                               Query as UsersQuery)
import graphql_jwt


# ===============================================================================
# All general schemas
class Query(UsersQuery, PostQuery,  graphene.ObjectType):
    pass


class Mutation(UsersMutation, PostMutation,  graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
# ===============================================================================
