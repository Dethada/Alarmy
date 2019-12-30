import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from backend.models import PersonAlert


class PersonAlertType(SQLAlchemyObjectType):
    class Meta:
        model = PersonAlert
        interfaces = (graphene.relay.Node, )