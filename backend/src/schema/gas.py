import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from src.models import Gas


class GasType(SQLAlchemyObjectType):
    class Meta:
        model = Gas
        interfaces = (graphene.relay.Node, )

class CustomGasType(graphene.ObjectType):
    capture_time = graphene.NonNull(graphene.types.datetime.DateTime)
    lpg = graphene.NonNull(graphene.Float)
    co = graphene.NonNull(graphene.Float)
    smoke = graphene.NonNull(graphene.Float)
