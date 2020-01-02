import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from src.models import Temperature


class TempType(SQLAlchemyObjectType):
    class Meta:
        model = Temperature
        interfaces = (graphene.relay.Node, )