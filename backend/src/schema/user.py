import graphene
from graphql import GraphQLError
from graphene_sqlalchemy import SQLAlchemyObjectType
from flask_jwt_extended import get_jwt_claims, get_jwt_identity, jwt_required
from argon2 import PasswordHasher
from src.models import User
from src.extensions import db


class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (graphene.relay.Node, )
        exclude_fields = ('password', )


class CreateUserMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        name = graphene.String(required=True)
        role = graphene.String(required=True)
        get_alerts = graphene.Boolean(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    @jwt_required
    def mutate(self, info, email, name, role, get_alerts, password):
        if get_jwt_claims()['role'] != 'Admin':
            raise GraphQLError('Admin permissions required.')

        if role not in ('Admin', 'User'):
            raise GraphQLError('Role must be Admin or User.')

        ph = PasswordHasher()
        user = User(email=email, name=name, role=role, get_alerts=get_alerts,
                    password=ph.hash(password))
        db.session.add(user)
        db.session.commit()
        return CreateUserMutation(user=user)


class UpdateUserMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String()
        name = graphene.String()
        role = graphene.String()
        get_alerts = graphene.Boolean()
        old_password = graphene.String()
        new_password = graphene.String()

    user = graphene.Field(UserType)

    @jwt_required
    def mutate(self, info, email=None, name=None, role=None, get_alerts=None, old_password=None, new_password=None):
        if get_jwt_claims()['role'] == 'Admin' and email and email != get_jwt_identity():
            user = User.query.filter_by(email=email).first()
            if name:
                user.name = name
            if role:
                user.role = role
            if get_alerts is not None:
                user.get_alerts = get_alerts
            if new_password:
                ph = PasswordHasher()
                user.password = ph.hash(new_password)

            db.session.commit()
        else:
            user = User.query.filter_by(email=get_jwt_identity()).first()
            ph = PasswordHasher()
            if name:
                user.name = name
            if get_alerts is not None:
                user.get_alerts = get_alerts
            if old_password and new_password and ph.verify(user.password, old_password):
                user.password = ph.hash(new_password)

            db.session.commit()
        return UpdateUserMutation(user=user)


class DeleteUserMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String()

    result = graphene.Field(graphene.String)

    @jwt_required
    def mutate(self, info, email):
        target_email = get_jwt_identity()
        if get_jwt_claims()['role'] == 'Admin' and email:
            target_email = email

        User.query.filter_by(email=target_email).delete()
        db.session.commit()

        return 'Deleted User {}'.format(target_email)
