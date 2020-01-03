from . import socketio
from flask_socketio import emit

# device_sid = ''

# @socketio.on('connect', namespace='/alert')
# def echo_socket():
#     try:
#         jwt_dict = decode_token(request.args.get('token').encode())
#         if jwt_dict['user_claims']['role'] == 'Device':
#             device_sid = request.sid
#             emit('serverMsg', jwt_dict)
#     except AttributeError:
#         pass

# '''
# { "iat": 1578036330, "nbf": 1578036330, "jti": "dc6f47b1-a962-4cc0-869a-640e84b52593", "identity": "admin@admin.com", "fresh": false, "type": "access", "user_claims": { "role": "Admin" } } 
# '''

@socketio.on('alert_users', namespace='/alert')
# @jwt_required
def alert_users(message):
    emit('alert', message, broadcast=True, include_self=False)

@socketio.on('new_values', namespace='/alert')
def update_device(message):
    emit('newValues', '', broadcast=True, include_self=False)
