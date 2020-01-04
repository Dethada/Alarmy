import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from src.models import EnvAlert
from src.extensions import db


class EnvAlertType(SQLAlchemyObjectType):
    class Meta:
        model = EnvAlert
        interfaces = (graphene.relay.Node, )


class DeleteEnvAlertMutation(graphene.Mutation):
    class Arguments:
        cid = graphene.Int(required=True)

    result = graphene.Field(graphene.String)

    def mutate(self, info, cid):
        EnvAlert.query.filter_by(cid=cid).delete()
        db.session.commit()

        return 'Deleted environment alert'
