from models import Platillo, Pedido, Pedido_Platillo, Platillo_Adimento, Pedido_Platillo_Adimento, Pedido_Ubicacion
from .bp import bp
from database import db
from auth.auth import get_active_session, active_session_decorator as active_session
from flask import Blueprint, request, Response, make_response, abort
from sqlalchemy import column, Integer, select
from sqlalchemy.sql import Values

#Recibes la lista de productos
#Creas la orden

#{
#productos: [{'id': X, adimentos: [X, X, X], 'cantidad': X}, ...],
#posible_ubicacion: null || {'coord_x': X, 'coord_y': Y}];
#
#}

@bp.route('/add', methods=['POST'])
@active_session
def add_order():
    #return {"response": "dedewd"}
    if not request.json:
        abort(400)

    productos = request.json.get("productos", None)

    if not isinstance(productos, list):
        abort(400)

    account_id = get_active_session().account_id
    if account_id is None:
        abort(400)

    pedido = Pedido(user_id=account_id, status=0)
    db.session.add(pedido)
    db.session.flush()

    ubicacion = request.json.get("ubicacion", None)

    if ubicacion is not None:
        if not all(isinstance(ubicacion.get(i, None), float) for i in ('coord_x', 'coord_y')):
            abort(400)

        ubicacion = Pedido_Ubicacion(pedido_id = pedido.id)
        db.session.add(ubicacion)

    for producto in productos:
        producto_id = producto.get("id", None)
        if not isinstance(producto_id, int):
            abort(400)

        if not db.session.query(Platillo.id).filter(Platillo.id == producto_id).scalar():
            return {
                'success':False,
                'reason': 'Invalid id',
                }, 404

        adimentos = producto.get("adimentos", None)
        if not isinstance(adimentos, list) or not all(isinstance(i, int) for i in adimentos):
            return {
                'success':False,
                'reason': 'Invalid adimento id',
                }, 404

        cantidad = producto.get('cantidad', None)
        if not isinstance(cantidad, int) or cantidad <= 0:
            abort(400)

        adimentos = db.session.query(Platillo_Adimento.c.id_adimento)\
                        .where(Platillo_Adimento.c.id_adimento.in_(adimentos))\
                        .all()
        
        platillo = Pedido_Platillo(pedido_id=pedido.id,
                                   platillo_id=producto_id,
                                   cantidad=cantidad,
                                   adimentos=[Pedido_Platillo_Adimento(adimento_id=i) for i, in adimentos])
        db.session.add(platillo)

    db.session.commit()
    return {'success': True}

