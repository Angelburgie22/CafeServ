from sqlalchemy import func
from sqlalchemy.orm import aliased
from database import db
from models import Dish, Ingredient, IngredientType, DishIngredientView, DishIngredientType
from .bp import bp


@bp.route('/dish_info/<int:dish_id>')
def info_dish(dish_id):
    session = db.session
    dish = session.get(Dish, dish_id)

    if dish is None:
        return '', 404

    ingredients = session.query(DishIngredientView.c.id_ingredient, DishIngredientView.c.name)\
                    .filter(DishIngredientView.c.id_dish == dish.id)

    result = {
            'success': True,
            'id': dish.id,
            'name': dish.name,
            'ingredients': [
                {
                    'id': id,
                    'name': name,
                } for id, name in ingredients.all()]
            }
    session.commit()
    return result

