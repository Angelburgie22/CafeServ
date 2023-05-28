from models import Platillo, Pedido, Pedido_Platillo, Platillo_Adimento, Pedido_Ubicacion
from .bp import bp
from database import db
from auth.auth import active_session_decorator as active_session
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

    productos = request.get("productos", None)
    print(productos)

    if not isinstance(productos, list):
        abort(400)

    ubicacion = request.get("ubicacion", None)
    pedido = Pedido(status='O')
    db.session.add(pedido)

    if ubicacion is not None:
        if not all(isinstance(ubicacion.get(i, None), float) for i in ('coord_x', 'coord_y')):
            abort(400)
        
        ubicacion = Pedido_Ubicacion(pedido_id = pedido.id)
        print(ubicacion)
        db.session.add(ubicacion)

    for producto in productos:
        producto_id = producto.get("id", None)
        print(producto_id)
        if not isinstance(producto_id, int):
            abort(400)

        if not db.session.query(db.session.query(Platillo.id).filter(Platillo.id == producto).exists()).scalar():
            return {
                'success':False,
                'reason': 'Invalid id',
                }, 404

        adimentos = producto.get("adimentos", None)
        print(adimentos)
        if not isinstance(adimentos, list) or not all(isinstance(i, int) for i in adimentos):
            return {
                'success':False,
                'reason': 'Invalid adimento id',
                }, 404
        
        v_adimentos = select(Values(column("id", "Integer"), name = "v").data([(i,) for i in adimentos])).subquery()

        adimentos = db.session.query(Platillo_Adimento.id)\
                .filter(select(v_adimentos.c.id).filter(Platillo_Adimento.platillo_id == v_adimentos.c.id).exists())\
                .all()
        
        platillo = Pedido_Platillo(pedido_id = pedido.id, adimentos = adimentos)
        print(platillo)
        db.session.add(platillo)

    return {'success': True}

