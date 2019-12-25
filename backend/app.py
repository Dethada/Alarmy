#!/usr/bin/env python3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .extensions import db, migrate, jwtmanager
from .views import blueprint

import argparse
import os
basedir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__.split('.')[0])
    app.debug = True  # Configs
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        os.path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['JWT_SECRET_KEY'] = 'super-secret'
    register_extensions(app)
    # register_routes(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    jwtmanager.init_app(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(blueprint)
    return None
