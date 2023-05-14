from flask import Flask, request, abort, redirect, url_for
from auth.session import bp as session_bp
from carta.info_platillos import bp as info_platillos_bp
import os
from database import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://mysql:{os.environ["MARIADB_PASSWD"]}@localhost/cafeserv?charset=utf8mb4'
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)

app.register_blueprint(session_bp)
app.register_blueprint(info_platillos_bp)

