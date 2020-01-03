#!/usr/bin/env python3
from src import create_app
from src.extensions import socketio
import logging

logging.basicConfig(level=logging.DEBUG)

app = create_app()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
