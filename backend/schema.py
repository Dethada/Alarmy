import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
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
        password = graphene.String(required=True)

    # The class attributes define the response of the mutation
    user = graphene.Field(UserType)

    def mutate(self, info, email, name, password):
        ph = PasswordHasher()
        user = User(email=email, name=name, role='user',
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
