import graphene
from graphql import GraphQLError
from graphene_sqlalchemy import SQLAlchemyObjectType
from flask_jwt_extended import get_jwt_claims, get_jwt_identity, jwt_required
from argon2 import PasswordHasher
from backend.models import User
from backend.extensions import db


class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (graphene.relay.Node, )
        exclude_fields = ('password', )


class CreateUserMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        email = graphene.String(required=True)
        name = graphene.String(required=True)
        role = graphene.String(required=True)
        password = graphene.String(required=True)

    # The class attributes define the response of the mutation
    user = graphene.Field(UserType)

    @jwt_required
    def mutate(self, info, email, name, role, password):
        if get_jwt_claims()['role'] != 'Admin':
            raise GraphQLError('Admin permissions required.')

        if role not in ('Admin', 'User'):
            raise GraphQLError('Role must be Admin or User.')

        ph = PasswordHasher()
        user = User(email=email, name=name, role=role,
                    password=ph.hash(password))
        db.session.add(user)
        db.session.commit()
        # Notice we return an instance of this mutation
        return CreateUserMutation(user=user)


class UpdateUserMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        email = graphene.String()
        name = graphene.String()
        role = graphene.String()
        old_password = graphene.String()
        new_password = graphene.String()

    # The class attributes define the response of the mutation
    user = graphene.Field(UserType)

    @jwt_required
    def mutate(self, info, email=None, name=None, role=None, old_password=None, new_password=None):
        if get_jwt_claims()['role'] == 'Admin' and email and email != get_jwt_identity():
            user = User.query.filter_by(email=email).first()
            if name:
                user.name = name
            if role:
                user.role = role
            if new_password:
                ph = PasswordHasher()
                user.password = ph.hash(new_password)

            db.session.commit()
            # Notice we return an instance of this mutation
            # return UpdateUserMutation(user=user)
        else:
            user = User.query.filter_by(email=get_jwt_identity()).first()
            ph = PasswordHasher()
            if name:
                user.name = name
            if old_password and new_password and ph.verify(user.password, old_password):
                user.password = ph.hash(new_password)

            db.session.commit()
            # Notice we return an instance of this mutation
        return UpdateUserMutation(user=user)


class DeleteUserMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        email = graphene.String()

    # The class attributes define the response of the mutation
    result = graphene.Field(graphene.String)

    @jwt_required
    def mutate(self, info, email):
        target_email = get_jwt_identity()
        if get_jwt_claims()['role'] == 'Admin' and email:
            target_email = email

        User.query.filter_by(email=target_email).delete()
        db.session.commit()

        return 'Deleted User {}'.format(target_email)
