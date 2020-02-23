import graphene
from graphql import GraphQLError
from graphene_sqlalchemy import SQLAlchemyObjectType
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models import Device, User
from src.extensions import socketio
from src.extensions import db
from src.utils import send_hware_config


class DeviceType(SQLAlchemyObjectType):
    class Meta:
        model = Device


class UpdateDeviceMutation(graphene.Mutation):
    class Arguments:
        poll_interval = graphene.Int()
        alert_interval = graphene.Int()
        alarm_duration = graphene.Int()
        alarm = graphene.Boolean()
        vflip = graphene.Boolean()
        motd = graphene.String()
        alarm_code = graphene.String()
        detect_humans = graphene.Boolean()
        temp_threshold = graphene.Int()

    device = graphene.Field(DeviceType)

    @jwt_required
    def mutate(self, info, poll_interval=None, alert_interval=None, alarm_duration=None, alarm=None, vflip=None, motd=None, alarm_code=None, detect_humans=None, temp_threshold=None):
        user = User.query.filter_by(email=get_jwt_identity()).first()
        device = Device.query.filter_by(device_id=user.device_id).first()
        config_dict = dict()
        if poll_interval:
            device.poll_interval = poll_interval
            config_dict['POLL_INTERVAL'] = poll_interval
        if alert_interval:
            device.alert_interval = alert_interval
            config_dict['ALERT_INTERVAL'] = alert_interval
        if alarm_duration:
            device.alarm_duration = alarm_duration
            config_dict['ALARM_DURATION'] = alarm_duration
        if motd:
            device.motd = motd
            config_dict['MOTD'] = motd
        if alarm_code:
            device.alarm_code = alarm_code
            config_dict['KEYPAD_CODE'] = alarm_code
        if temp_threshold:
            device.temp_threshold = temp_threshold
            config_dict['TEMP_THRESHOLD'] = temp_threshold
        if alarm is not None:
            device.alarm = alarm
            config_dict['ALARM_ON'] = alarm
        if vflip is not None:
            device.vflip = vflip
            config_dict['VFLIP'] = vflip
        if detect_humans is not None:
            device.detect_humans = detect_humans
            config_dict['DETECT_HUMANS'] = detect_humans

        db.session.commit()
        if user.device_id:
            send_hware_config(user.device_id, config_dict)

        return UpdateDeviceMutation(device=device)

class RegisterDeviceMutation(graphene.Mutation):
    class Arguments:
        device_id = graphene.String(required=True)
    
    device = graphene.Field(DeviceType)

    @jwt_required
    def mutate(self, info, device_id):
        device = Device.query.filter_by(device_id=device_id).first()
        if device:
            user = User.query.filter_by(email=get_jwt_identity()).first()
            user.device_id = device.device_id
            db.session.commit()
            return RegisterDeviceMutation(device=device)
        raise GraphQLError('Invalid Device ID')

class DeregisterDeviceMutation(graphene.Mutation):
    
    result = graphene.String()

    @jwt_required
    def mutate(self, info):
        user = User.query.filter_by(email=get_jwt_identity()).first()
        user.device_id = None
        db.session.commit()
        return 'Ok'
