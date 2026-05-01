from app import create_app
from database import db
from models import UserAccount, UserLoginInfo, UserSession, CSRFToken, Dish, IngredientType, Ingredient, DishIngredient, DishIngredientType
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    # Sample Users
    user1 = UserAccount(
        id=1,
        creation_time=datetime(2023, 1, 1, 0, 0, 0),
        status=1,
        email='alice@example.com',
        username='alice',
        first_name='Alice',
        last_name='Smith'
    )
    user2 = UserAccount(
        id=2,
        creation_time=datetime(2023, 1, 2, 0, 0, 0),
        status=1,
        email='bob@example.com',
        username='bob',
        first_name='Bob',
        last_name='Johnson'
    )
    db.session.add(user1)
    db.session.add(user2)

    # Passwords: 'password123' hashed
    login1 = UserLoginInfo(account_id=1, passwd_hash=generate_password_hash('password123'))
    login2 = UserLoginInfo(account_id=2, passwd_hash=generate_password_hash('password123'))
    db.session.add(login1)
    db.session.add(login2)

    # Ingredient Types
    bread_type = IngredientType(id=1, name='Bread')
    meat_type = IngredientType(id=2, name='Meat')
    cheese_type = IngredientType(id=3, name='Cheese')
    veg_type = IngredientType(id=4, name='Vegetables')
    db.session.add(bread_type)
    db.session.add(meat_type)
    db.session.add(cheese_type)
    db.session.add(veg_type)

    # Ingredients
    ingredients = [
        Ingredient(id=1, type_id=1, name='Wheat Bread'),
        Ingredient(id=2, type_id=1, name='Integral Bread'),
        Ingredient(id=3, type_id=1, name='Rye Bread'),
        Ingredient(id=4, type_id=2, name='Chicken'),
        Ingredient(id=5, type_id=2, name='Beef'),
        Ingredient(id=6, type_id=2, name='Pork'),
        Ingredient(id=7, type_id=3, name='Cheddar'),
        Ingredient(id=8, type_id=3, name='Mozzarella'),
        Ingredient(id=9, type_id=3, name='Swiss'),
        Ingredient(id=10, type_id=4, name='Lettuce'),
        Ingredient(id=11, type_id=4, name='Tomato'),
        Ingredient(id=12, type_id=4, name='Onion'),
    ]
    db.session.add_all(ingredients)

    # Dishes
    sandwich = Dish(id=1, name='Sandwich', description='A delicious sandwich')
    salad = Dish(id=2, name='Salad', description='Fresh garden salad')
    pizza = Dish(id=3, name='Pizza', description='Cheesy pizza')
    db.session.add(sandwich)
    db.session.add(salad)
    db.session.add(pizza)

    # DishIngredientType: which types are allowed for each dish
    dish_types = [
        DishIngredientType(dish_id=1, ingredient_type_id=1),  # Sandwich: Bread
        DishIngredientType(dish_id=1, ingredient_type_id=2),  # Meat
        DishIngredientType(dish_id=1, ingredient_type_id=3),  # Cheese
        DishIngredientType(dish_id=1, ingredient_type_id=4),  # Vegetables
        DishIngredientType(dish_id=2, ingredient_type_id=3),  # Salad: Cheese
        DishIngredientType(dish_id=2, ingredient_type_id=4),  # Vegetables
        DishIngredientType(dish_id=3, ingredient_type_id=2),  # Pizza: Meat
        DishIngredientType(dish_id=3, ingredient_type_id=3),  # Cheese
        DishIngredientType(dish_id=3, ingredient_type_id=4),  # Vegetables
    ]
    db.session.add_all(dish_types)

    # DishIngredient: specific allowed ingredients (for now, allow all in types)
    # Since the view unions allowed and type-based, but for DishIngredient, if not specified, allowed via type
    # For simplicity, add some restrictions, e.g., Sandwich doesn't allow Pork
    dish_ings = [
        DishIngredient(dish_id=1, ingredient_id=6, allowed=False),  # Sandwich no Pork
        # Others allowed by default via types
    ]
    db.session.add_all(dish_ings)

    db.session.commit()

print("Sample data inserted successfully!")