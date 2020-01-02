import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from src.models import Gas


class GasType(SQLAlchemyObjectType):
    class Meta:
        model = Gas
        interfaces = (graphene.relay.Node, )