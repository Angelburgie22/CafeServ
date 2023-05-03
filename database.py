from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)
Model = db.Model

