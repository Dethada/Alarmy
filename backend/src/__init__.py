#!/usr/bin/env python3
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from argon2 import PasswordHasher
from .extensions import db, migrate, jwtmanager, cors, socketio
from flask_jwt_extended import jwt_required
from .views import blueprint
from .models import User
from . import events  # required to load the websocket events
from dotenv import load_dotenv
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__.split('.')[0])
    app.debug = True  # Configs
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['JWT_SECRET_KEY'] = 'super-secret'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)
    jwtmanager.init_app(app)
    socketio.init_app(app)
    cors.init_app(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(blueprint)
