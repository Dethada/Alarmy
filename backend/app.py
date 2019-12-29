#!/usr/bin/env python3
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from argon2 import PasswordHasher
from .extensions import db, migrate, jwtmanager, cors
from .views import blueprint
from .models import User
basedir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__.split('.')[0])
    app.debug = True  # Configs
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://alarmyuser:verysecurepassword123@192.168.1.17/alarmy'
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['JWT_SECRET_KEY'] = 'super-secret'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
    # app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'
    # app.config['JWT_COOKIE_CSRF_PROTECT'] = True
    # app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    # app.config['JWT_COOKIE_SECURE'] = False # False to allow JWT cookies to be sent over http.
    register_extensions(app)
    register_blueprints(app)
    # create_initial_admin()
    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)
    jwtmanager.init_app(app)
    cors.init_app(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(blueprint)
    return None
