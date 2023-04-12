from flask import Flask, request, abort, redirect, url_for
from auth.session import bp as session_bp
from database import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)

app.register_blueprint(session_bp)

