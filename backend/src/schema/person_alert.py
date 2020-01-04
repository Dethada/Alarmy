import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from src.models import PersonAlert
from src.extensions import db


class PersonAlertType(SQLAlchemyObjectType):
    class Meta:
        model = PersonAlert
        interfaces = (graphene.relay.Node, )


class DeletePersonAlertMutation(graphene.Mutation):
    class Arguments:
        cid = graphene.Int(required=True)

    result = graphene.Field(graphene.String)

    def mutate(self, info, cid):
        PersonAlert.query.filter_by(cid=cid).delete()
        db.session.commit()

        return 'Deleted person alert'
