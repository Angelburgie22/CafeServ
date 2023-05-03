from database import metadata, db
import models
from app import app

with app.app_context():
    metadata.create_all(bind=db.engine)

