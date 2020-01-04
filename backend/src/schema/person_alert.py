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
        # The input arguments for this mutation
        cid = graphene.Int(required=True)

    # The class attributes define the response of the mutation
    result = graphene.Field(graphene.String)

    def mutate(self, info, cid):
        PersonAlert.query.filter_by(cid=cid).delete()
        db.session.commit()

        return 'Deleted person alert'
