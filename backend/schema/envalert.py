import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from backend.models import EnvAlert


class EnvAlertType(SQLAlchemyObjectType):
    class Meta:
        model = EnvAlert
        interfaces = (graphene.relay.Node, )