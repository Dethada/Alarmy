from . import socketio
from flask_socketio import emit
from flask import Flask, render_template, session, request, \
    copy_current_request_context
from flask_socketio import emit, join_room, leave_room, \
    close_room, rooms, disconnect
from flask_jwt_extended import jwt_required

@socketio.on('connect', namespace='/alert')
def echo_socket():
    emit('my response', {'data': 'Connected'})

@socketio.on('message', namespace='/alert')
def handle_message(message):
    print('received message: ', message)

# ================================================

@socketio.on('my_event', namespace='/alert')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('my_broadcast_event', namespace='/alert')
@jwt_required
def test_broadcast_message(message):
    # session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response', message,
         broadcast=True)


@socketio.on('join', namespace='/alert')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('leave', namespace='/alert')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('close_room', namespace='/alert')
def close(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])


@socketio.on('my_room_event', namespace='/alert')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio.on('disconnect_request', namespace='/alert')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    # for this emit we use a callback function
    # when the callback function is invoked we know that the message has been
    # received and it is safe to disconnect
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)


@socketio.on('my_ping', namespace='/alert')
def ping_pong():
    emit('my_pong')


@socketio.on('disconnect', namespace='/alert')
def test_disconnect():
    print('Client disconnected', request.sid)