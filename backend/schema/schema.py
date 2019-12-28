import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField
from backend.schema.user import *


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_users = SQLAlchemyConnectionField(UserType)
    # all_users = graphene.List(UserType)
    user_info = graphene.Field(UserType)

    @jwt_required
    def resolve_user_info(self, info):
        return User.query.filter_by(email=get_jwt_identity()).first()


class Mutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()
    update_user = UpdateUserMutation.Field()
    delete_user = DeleteUserMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
