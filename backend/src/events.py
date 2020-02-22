from . import socketio
from flask import request
from flask_socketio import emit, join_room
from .models import User
from flask_jwt_extended import decode_token, get_jwt_claims

@socketio.on('alert_users', namespace='/alert')
def alert_users(message):
    emit('alert', message, broadcast=True, include_self=False)


@socketio.on('connect')
def on_join():
    token = request.args.get('token')
    if token:
        decoded_token = decode_token(token)
        user = User.query.filter_by(email=decoded_token['identity']).first()
        room = user.device_id
        if room:
            join_room(room)
            print(f'User {user.name} joined {user.device_id}')
