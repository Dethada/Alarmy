from . import socketio
from flask import request
from flask_socketio import join_room, ConnectionRefusedError
from .models import User
from flask_jwt_extended import decode_token, get_jwt_claims

@socketio.on('connect')
def on_join():
    token = request.args.get('token')
    if token:
        try:
            decoded_token = decode_token(token)
            user = User.query.filter_by(email=decoded_token['identity']).first()
            room = user.device_id
            print(user.device_id)
            if room:
                join_room(room)
                print(f'User {user.name} joined {user.device_id}')
        except Exception:
            # on any jwt error
            raise ConnectionRefusedError('unauthorized!')
    else:
        raise ConnectionRefusedError('unauthorized!')
