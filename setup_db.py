from database import metadata, db
import models
from app import create_app
import sqlalchemy

temp_config = {
    'database_uri': f'mysql+pymysql://root:{__import__("os").environ["MARIADB_PASSWD"]}@localhost?charset=utf8mb4',
    'database_echo': True,
    'flask_app_name': 'temp'
}

temp_app = create_app(temp_config)

with temp_app.app_context():
    db.session.execute(sqlalchemy.text('CREATE DATABASE IF NOT EXISTS cafeserv'))

app = create_app()

with app.app_context():
    metadata.create_all(bind=db.engine)

