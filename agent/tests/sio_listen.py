import socketio

# standard Python
sio = socketio.Client()

sio.connect('http://localhost:5000', namespaces=['/alert'])

@sio.on('my_response', namespace='/alert')
def on_message(data):
    print('I received a message!', data)

print('my sid is', sio.sid)

# sio.emit('message', {'foo': 'bar'})
sio.wait()