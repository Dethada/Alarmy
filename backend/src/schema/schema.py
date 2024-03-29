from datetime import datetime, timedelta
import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField
import pandas as pd
from src.models import Device, Temperature, Gas, PersonAlert, EnvAlert
from src.schema.user import *
from src.schema.gas import CustomGasType
from src.schema.temp import CustomTempType
from src.schema.env_alert import EnvAlertType, DeleteEnvAlertMutation
from src.schema.person_alert import PersonAlertType, DeletePersonAlertMutation
from src.schema.device import DeviceType, UpdateDeviceMutation, RegisterDeviceMutation, DeregisterDeviceMutation
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
    # user_test = graphene.Field(UserType, email=graphene.String(required=True))

    @jwt_required
    def resolve_user_info(self, info):
        return User.query.filter_by(email=get_jwt_identity()).first()

    @jwt_required
    def resolve_device_info(self, info):
        user = User.query.filter_by(email=get_jwt_identity()).first()
        return user.device

    @jwt_required
    def resolve_all_envalert(self, info):
        user = User.query.filter_by(email=get_jwt_identity()).first()
        return EnvAlert.query.filter_by(device_id=user.device_id)

    @jwt_required
    def resolve_all_person_alert(self, info):
        user = User.query.filter_by(email=get_jwt_identity()).first()
        return PersonAlert.query.filter_by(device_id=user.device_id)

    @jwt_required
    def resolve_person_alert(self, info, cid):
        user = User.query.filter_by(email=get_jwt_identity()).first()
        return PersonAlert.query.filter_by(cid=cid, device_id=user.device_id).first()

    @jwt_required
    def resolve_all_temp(self, info, duration=''):
        user = User.query.filter_by(email=get_jwt_identity()).first()
        if duration == '24H':
            since = datetime.now() - timedelta(hours=24)
            df = analysis_helper(Temperature.query.filter(
                Temperature.device_id == user.device_id, Temperature.capture_time > since).statement, 'H')
            result = [CustomTempType(capture_time=time, value=value)
                      for time, value in zip(df.index, df['value'])]
        elif duration == '7D':
            since = datetime.now() - timedelta(days=7)
            df = analysis_helper(Temperature.query.filter(
                Temperature.device_id == user.device_id, Temperature.capture_time > since).statement, '4H')
            result = [CustomTempType(capture_time=time, value=value)
                      for time, value in zip(df.index, df['value'])]
        elif duration == '30D':
            since = datetime.now() - timedelta(days=30)
            df = analysis_helper(Temperature.query.filter(
                Temperature.device_id == user.device_id, Temperature.capture_time > since).statement, 'D')
            result = [CustomTempType(capture_time=time, value=value)
                      for time, value in zip(df.index, df['value'])]
        elif duration == 'ALL':
            df = analysis_helper(Temperature.query.filter(
                Temperature.device_id == user.device_id).statement, '2W')
            result = [CustomTempType(capture_time=time, value=value)
                      for time, value in zip(df.index, df['value'])]
        else:
            result = [CustomTempType(capture_time=x.capture_time, value=x.value)
                      for x in Temperature.query.filter(Temperature.device_id == user.device_id).order_by(Temperature.capture_time.desc()).limit(20)]
        return result

    @jwt_required
    def resolve_all_gas(self, info, duration=''):
        user = User.query.filter_by(email=get_jwt_identity()).first()
        result = []
        if duration == '24H':
            since = datetime.now() - timedelta(hours=24)
            df = analysis_helper(Gas.query.filter(
                Gas.device_id == user.device_id, Gas.capture_time > since).statement, 'H')
            for row in df.itertuples():
                result.append(CustomGasType(capture_time=row.Index,
                                            lpg=row.lpg, co=row.co, smoke=row.smoke))
        elif duration == '7D':
            since = datetime.now() - timedelta(days=7)
            df = analysis_helper(Gas.query.filter(
                Gas.device_id == user.device_id, Gas.capture_time > since).statement, '4H')
            for row in df.itertuples():
                result.append(CustomGasType(capture_time=row.Index,
                                            lpg=row.lpg, co=row.co, smoke=row.smoke))
        elif duration == '30D':
            since = datetime.now() - timedelta(days=30)
            df = analysis_helper(Gas.query.filter(
                Gas.device_id == user.device_id, Gas.capture_time > since).statement, 'D')
            for row in df.itertuples():
                result.append(CustomGasType(capture_time=row.Index,
                                            lpg=row.lpg, co=row.co, smoke=row.smoke))
        elif duration == 'ALL':
            df = analysis_helper(Gas.query.filter(
                Gas.device_id == user.device_id).statement, '2W')
            for row in df.itertuples():
                result.append(CustomGasType(capture_time=row.Index,
                                            lpg=row.lpg, co=row.co, smoke=row.smoke))
        else:
            result = [CustomGasType(capture_time=x.capture_time, lpg=x.lpg, co=x.co, smoke=x.smoke)
                      for x in Gas.query.filter(Gas.device_id == user.device_id).order_by(Gas.capture_time.desc()).limit(20)]
        return result


class Mutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()
    update_user = UpdateUserMutation.Field()
    delete_user = DeleteUserMutation.Field()
    update_device = UpdateDeviceMutation.Field()
    register_device = RegisterDeviceMutation.Field()
    deregister_device = DeregisterDeviceMutation.Field()
    delete_person_alert = DeletePersonAlertMutation.Field()
    delete_env_alert = DeleteEnvAlertMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
