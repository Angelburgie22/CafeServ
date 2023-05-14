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

    por_id = session.query(Adimento, Platillo_Adimento.allowed)\
                    .join(Platillo_Adimento).join(Platillo)\
                    .filter(Platillo.id == platillo.id)

    por_tipo = session.query(Adimento, True)\
                    .join(TipoAdimento).join(Platillo_TipoAdimento).join(Platillo)\
                    .filter(Platillo.id == platillo.id)

    adimentos_q = por_id.union(por_tipo)\
                    .group_by(Adimento.id)\
                    .having(func.min(Platillo_Adimento.allowed))

    result = {
            'id': platillo.id,
            'nombre': platillo.nombre,
            'adimentos': [
                           {
                               'id': adimento.id,
                               'nombre': adimento.nombre,
                           } for adimento, b in adimentos_q.all()]
            }
    session.commit()
    return result

