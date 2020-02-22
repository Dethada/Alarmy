#!/usr/bin/env python3
from src import create_app
from src.extensions import socketio
import argparse
import logging

logging.basicConfig(level=logging.DEBUG)

app = create_app()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Backend for Alarmy')
    parser.add_argument('-p', '--port', type=int, default=5000, help="(default: %(default)s)")
    args = parser.parse_args()
    socketio.run(app, host='0.0.0.0', port=args.port)
