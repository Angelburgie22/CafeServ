import pytest
import sqlalchemy
from sqlalchemy import func
from werkzeug.security import generate_password_hash
import os
from app import create_app, default_config
from database import db, metadata
from models import *

@pytest.fixture
def app():
    app = create_app(default_config | {
        'database_uri': f'mysql+pymysql://root:{os.environ["MARIADB_PASSWD"]}@localhost/test_cafeserv?charset=utf8mb4',
    })

    with app.app_context():
        session = db.session
        session.execute(sqlalchemy.text('DROP DATABASE test_cafeserv'))
        session.execute(sqlalchemy.text('CREATE DATABASE test_cafeserv'))
        session.execute(sqlalchemy.text('USE test_cafeserv'))

        metadata.create_all(bind=db.engine)

        users = [
                {
                    'status': 0,
                    'username': 'victor22',
                    'email': 'victor@torres.com',
                    'first_name': 'victor',
                    'last_name': 'torres',
                },
        ]

        for kw in users:
            user = UserAccount(creation_time=func.now(), **kw)
            passwd_hash = generate_password_hash('hola' + kw['first_name'])
            user_login = UserLoginInfo(passwd_hash=passwd_hash, account=user)
            session.add(user)

        milk_type = IngredientType(name='Milk')

        whole_milk = Ingredient(name='Whole Milk', type=milk_type)
        raw_milk = Ingredient(name='Raw Milk', type=milk_type)
        lactose_free_milk = Ingredient(name='Lactose-free Milk', type=milk_type)
        semi_skimmed_milk = Ingredient(name='Semi-skimmed Milk', type=milk_type)

        session.add(milk_type)

        crepe = Dish(name='Crepe')
        session.add(DishIngredientType(dish=crepe, ingredient_type=milk_type))
        session.add(DishIngredient(dish=crepe, ingredient=semi_skimmed_milk, allowed=False))

        coffee = Dish(name='Coffee')
        session.add(DishIngredient(dish=coffee, ingredient=whole_milk, allowed=True))
        session.add(DishIngredient(dish=coffee, ingredient=lactose_free_milk, allowed=True))
        session.add(DishIngredient(dish=coffee, ingredient=semi_skimmed_milk, allowed=True))

        eggs = Dish(name='Eggs')

        session.add(crepe)
        session.add(coffee)
        session.add(eggs)

        session.commit()

        yield app

