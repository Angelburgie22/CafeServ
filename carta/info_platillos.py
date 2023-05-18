from sqlalchemy import func
from sqlalchemy.orm import aliased
from database import db
from models import Platillo, Adimento, TipoAdimento, Platillo_Adimento, Platillo_TipoAdimento
from .bp import bp


@bp.route('/info_platillo/<int:platillo_id>')
def info_platillo(platillo_id):
    session = db.session
    platillo = session.get(Platillo, platillo_id)

    if platillo is None:
        return '', 404

    adimentos = session.query(Platillo_Adimento.c.id_adimento, Platillo_Adimento.c.nombre)\
                    .filter(Platillo_Adimento.c.id_platillo == platillo.id)

    result = {
            'id': platillo.id,
            'nombre': platillo.nombre,
            'adimentos': [
                           {
                               'id': id,
                               'nombre': nombre,
                           } for id, nombre in adimentos.all()]
            }
    session.commit()
    return result

