import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from src.models import Device
from src.extensions import socketio
from src.extensions import db
from flask_jwt_extended import jwt_required


class DeviceType(SQLAlchemyObjectType):
    class Meta:
        model = Device


class UpdateDeviceMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        poll_interval = graphene.Int()
        alert_interval = graphene.Int()
        alarm_duration = graphene.Int()
        alarm = graphene.Boolean()
        email = graphene.String()
        vflip = graphene.Boolean()
        motd = graphene.String()
        alarm_code = graphene.String()

    # The class attributes define the response of the mutation
    device = graphene.Field(DeviceType)

    def mutate(self, info, poll_interval=None, alert_interval=None, alarm_duration=None, alarm=None, email=None, vflip=None, motd=None, alarm_code=None):
        device = Device.query.first()
        if poll_interval:
            device.poll_interval = poll_interval
        if alert_interval:
            device.alert_interval = alert_interval
        if alarm_duration:
            device.alarm_duration = alarm_duration
        if email:
            device.email = email
        if motd:
            device.motd = motd
        if alarm_code:
            device.alarm_code = alarm_code
        if alarm is not None:
            device.alarm = alarm
        if vflip is not None:
            device.vflip = vflip

        db.session.commit()
        socketio.emit('update_device', '', broadcast=True, namespace='/device')
        
        return UpdateDeviceMutation(device=device)
