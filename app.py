from flask import Flask, request, abort, redirect, url_for
from auth.session import bp as session_bp
from carta.info_platillos import bp as info_platillos_bp
import os
from database import db

default_config = {
        'database_uri': f'sqlite:///database.db',
        'database_echo': True,
        'flask_app_name': __name__
        }

def create_app(config=default_config):
    app = Flask(config['flask_app_name'])

    app.config['SQLALCHEMY_DATABASE_URI'] = config['database_uri']
    app.config['SQLALCHEMY_ECHO'] = config['database_echo']

    db.init_app(app)

    app.register_blueprint(session_bp)
    app.register_blueprint(info_platillos_bp)

    return app

