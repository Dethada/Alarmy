from . import socketio
from flask_socketio import emit


@socketio.on('alert_users', namespace='/alert')
# @jwt_required
def alert_users(message):
    emit('alert', message, broadcast=True, include_self=False)


@socketio.on('new_values', namespace='/alert')
def update_device(message):
    emit('newValues', '', broadcast=True, include_self=False)
