import graphene
from graphql import GraphQLError
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_jwt_extended import get_jwt_claims, get_jwt_identity, jwt_required
from argon2 import PasswordHasher
from .models import User
from .extensions import db


class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (graphene.relay.Node, )
        exclude_fields = ('password', )


class UserMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        email = graphene.String(required=True)
        name = graphene.String(required=True)
        role = graphene.String(required=True)
        password = graphene.String(required=True)

    # The class attributes define the response of the mutation
    user = graphene.Field(UserType)

    # @anonymous_return(AuthenticationRequired.default_message)
    @jwt_required
    def mutate(self, info, email, name, role, password):
        if get_jwt_claims()['role'] != 'Admin':
            raise GraphQLError('Admin permissions required.')
        ph = PasswordHasher()
        user = User(email=email, name=name, role=role,
                    password=ph.hash(password))
        db.session.add(user)
        db.session.commit()
        # Notice we return an instance of this mutation
        return UserMutation(user=user)


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_users = SQLAlchemyConnectionField(UserType)


class Mutation(graphene.ObjectType):
    create_user = UserMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
