import pytest
import sqlalchemy
from werkzeug.security import generate_password_hash
import os
from app import create_app, default_config
from database import db, metadata
from models import *

@pytest.fixture
def app():
    app = create_app(default_config | {
        'database_uri': f'sqlite:///test_database.db',
    })

    with app.app_context():
        session = db.session
        metadata.drop_all(bind=db.engine)
        metadata.create_all(bind=db.engine)

        users = [
                {
                    'status': 0,
                    'username': 'victor22',
                    'email': 'victor@torres.com',
                    'nombre': 'victor',
                    'apellido_p': 'torres',
                },
        ]

        for kw in users:
            user = UserAccount(creation_time=func.now(), **kw)
            passwd_hash = generate_password_hash('hola' + kw['nombre'])
            user_login = UserLoginInfo(passwd_hash=passwd_hash, account=user)
            session.add(user)

        tipo_leche = TipoAdimento(nombre='Leche')

        leche_entera = Adimento(nombre='Leche entera', tipo_adimento=tipo_leche)
        leche_bronca = Adimento(nombre='Leche bronca', tipo_adimento=tipo_leche)
        leche_deslact = Adimento(nombre='Leche deslactosada', tipo_adimento=tipo_leche)
        leche_semides = Adimento(nombre='Leche semideslactosada', tipo_adimento=tipo_leche)

        session.add(tipo_leche)

        crepa = Platillo(nombre='Crepa')
        session.add(Platillo_TipoAdimento(platillo=crepa, tipo_adimento=tipo_leche))
        session.add(Platillo_UnAdimento(platillo=crepa, adimento=leche_semides, allowed=False))

        cafe = Platillo(nombre='Café')
        session.add(Platillo_UnAdimento(platillo=cafe, adimento=leche_entera, allowed=True))
        session.add(Platillo_UnAdimento(platillo=cafe, adimento=leche_deslact, allowed=True))
        session.add(Platillo_UnAdimento(platillo=cafe, adimento=leche_semides, allowed=True))

        huevos = Platillo(nombre='Huevos')

        session.add(crepa)
        session.add(cafe)
        session.add(huevos)

        session.commit()

        yield app

