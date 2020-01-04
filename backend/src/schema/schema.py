from datetime import datetime, timedelta
import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField
import pandas as pd
from src.models import Device, Temperature, Gas, PersonAlert
from src.schema.user import *
from src.schema.gas import CustomGasType
from src.schema.temp import CustomTempType
from src.schema.env_alert import EnvAlertType, DeleteEnvAlertMutation
from src.schema.person_alert import PersonAlertType, DeletePersonAlertMutation
from src.schema.device import DeviceType, UpdateDeviceMutation
from src.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity


def analysis_helper(query_statement, frequency):
    df = pd.read_sql(query_statement, db.session.bind)
    df['capture_time'] = pd.to_datetime(df['capture_time'])
    df.index = df['capture_time']
    df = df.resample(frequency).mean().dropna()
    return df


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_users = SQLAlchemyConnectionField(UserType)
    user_info = graphene.Field(UserType)
    all_gas = graphene.List(CustomGasType, duration=graphene.String())
    device_info = graphene.Field(DeviceType)
    all_temp = graphene.List(CustomTempType, duration=graphene.String())
    all_envalert = SQLAlchemyConnectionField(EnvAlertType)
    all_person_alert = SQLAlchemyConnectionField(PersonAlertType)
    person_alert = graphene.Field(
        PersonAlertType, cid=graphene.Int(required=True))
    user_test = graphene.Field(UserType, email=graphene.String(required=True))

    @jwt_required
    def resolve_user_info(self, info):
        return User.query.filter_by(email=get_jwt_identity()).first()

    def resolve_user_test(self, info, email):
        return User.query.filter_by(email=email).first()

    def resolve_device_info(self, info):
        return Device.query.first()

    def resolve_person_alert(self, info, cid):
        return PersonAlert.query.filter_by(cid=cid).first()

    def resolve_all_temp(self, info, duration=''):
        if duration == '24H':
            since = datetime.now() - timedelta(hours=24)
            df = analysis_helper(Temperature.query.filter(
                Temperature.capture_time > since).statement, 'H')
            result = [CustomTempType(capture_time=time, value=value)
                      for time, value in zip(df.index, df['value'])]
        elif duration == '7D':
            since = datetime.now() - timedelta(days=7)
            df = analysis_helper(Temperature.query.filter(
                Temperature.capture_time > since).statement, '4H')
            result = [CustomTempType(capture_time=time, value=value)
                      for time, value in zip(df.index, df['value'])]
        elif duration == '30D':
            since = datetime.now() - timedelta(days=30)
            df = analysis_helper(Temperature.query.filter(
                Temperature.capture_time > since).statement, 'D')
            result = [CustomTempType(capture_time=time, value=value)
                      for time, value in zip(df.index, df['value'])]
        elif duration == 'ALL':
            df = analysis_helper(Temperature.query.statement, '2W')
            result = [CustomTempType(capture_time=time, value=value)
                      for time, value in zip(df.index, df['value'])]
        else:
            result = [CustomTempType(capture_time=x.capture_time, value=x.value)
                      for x in Temperature.query.order_by(Temperature.capture_time.desc()).limit(20)]
        return result

    def resolve_all_gas(self, info, duration=''):
        result = []
        if duration == '24H':
            since = datetime.now() - timedelta(hours=24)
            df = analysis_helper(Gas.query.filter(
                Gas.capture_time > since).statement, 'H')
            for row in df.itertuples():
                result.append(CustomGasType(capture_time=row.Index,
                                            lpg=row.lpg, co=row.co, smoke=row.smoke))
        elif duration == '7D':
            since = datetime.now() - timedelta(days=7)
            df = analysis_helper(Gas.query.filter(
                Gas.capture_time > since).statement, '4H')
            for row in df.itertuples():
                result.append(CustomGasType(capture_time=row.Index,
                                            lpg=row.lpg, co=row.co, smoke=row.smoke))
        elif duration == '30D':
            since = datetime.now() - timedelta(days=30)
            df = analysis_helper(Gas.query.filter(
                Gas.capture_time > since).statement, 'D')
            for row in df.itertuples():
                result.append(CustomGasType(capture_time=row.Index,
                                            lpg=row.lpg, co=row.co, smoke=row.smoke))
        elif duration == 'ALL':
            df = analysis_helper(Gas.query.statement, '2W')
            for row in df.itertuples():
                result.append(CustomGasType(capture_time=row.Index,
                                            lpg=row.lpg, co=row.co, smoke=row.smoke))
        else:
            result = [CustomGasType(capture_time=x.capture_time, lpg=x.lpg, co=x.co, smoke=x.smoke)
                      for x in Gas.query.order_by(Gas.capture_time.desc()).limit(20)]
        return result


class Mutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()
    update_user = UpdateUserMutation.Field()
    delete_user = DeleteUserMutation.Field()
    update_device = UpdateDeviceMutation.Field()
    delete_person_alert = DeletePersonAlertMutation.Field()
    delete_env_alert = DeleteEnvAlertMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
