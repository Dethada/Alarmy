import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField
from src.models import Device
from src.schema.user import *
from src.schema.gas import GasType
from src.schema.temp import TempType
from src.schema.env_alert import EnvAlertType
from src.schema.person_alert import PersonAlertType
from src.schema.device import DeviceType, UpdateDeviceMutation


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_users = SQLAlchemyConnectionField(UserType)
    # all_users = graphene.List(UserType)
    user_info = graphene.Field(UserType)
    all_gas = SQLAlchemyConnectionField(GasType)
    device_info = graphene.Field(DeviceType)
    all_temp = SQLAlchemyConnectionField(TempType)
    all_envalert = SQLAlchemyConnectionField(EnvAlertType)
    all_person_alert = SQLAlchemyConnectionField(PersonAlertType)
    user_test = graphene.Field(UserType, email=graphene.String(required=True))


    @jwt_required
    def resolve_user_info(self, info):
        return User.query.filter_by(email=get_jwt_identity()).first()
    
    def resolve_user_test(self, info, email):
        return User.query.filter_by(email=email).first()
    
    def resolve_device_info(self, info):
        return Device.query.first()


class Mutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()
    update_user = UpdateUserMutation.Field()
    delete_user = DeleteUserMutation.Field()
    update_device = UpdateDeviceMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
