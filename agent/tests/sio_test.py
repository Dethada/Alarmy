import socketio

# standard Python
sio = socketio.Client()

sio.connect('http://localhost:5000', namespaces=['/alert'])

@sio.on('serverMsg', namespace='/alert')
def on_message(data):
    print('I received a message!', data)

print('my sid is', sio.sid)

msg = ''
while msg != 'q':
    msg = input('> ')
    sio.emit('alert_users', msg, namespace='/alert')
