from database import metadata, db
import models
from app import create_app

with create_app().app_context():
    metadata.create_all(bind=db.engine)

