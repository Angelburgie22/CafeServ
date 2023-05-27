from flask import Blueprint, request, Response, make_response, abort
import werkzeug.exceptions
from .csrf_token import check_csrf_token, generate_csrf_token
from .auth import create_user_session, close_active_session, active_session_decorator as active_session
from database import db

bp = Blueprint('api_session', __name__, url_prefix='/api/session')

@bp.route('/create', methods=['POST'])
def create():
    if not request.json:
        abort(400)
    if any(i not in request.json or
            not isinstance(request.json[i], str) for i in ('user', 'passwd', 'token')):
        abort(400)

    user = request.json['user']
    passwd = request.json['passwd']
    csrf_token = request.json['token']

    with db.session() as session:
        # El uso de token CSRF es más común en aplicaciones HTML, debido a ataques CSRF.
        # Aquí se añade para una futura compatibilidad web y protección extra.
        if not check_csrf_token(csrf_token):
            session.commit()
            return {'success': False, 'reason':'Invalid login request token'}, 400

        user_session = create_user_session(user, passwd)
        if user_session is None:
            session.commit()
            return {'success': False, 'reason':'Invalid credentials'}, 401

        token = user_session.id
        session.commit()

    response = make_response({'success':True, 'identifier':'cookies'})
    response.set_cookie('sid', secure=True, httponly=True, value=token)

    return response

@bp.route('/close', methods=['DELETE'])
@active_session
def close():
    with db.session() as session:
        close_active_session()
        session.commit()

    response = Response(status=204) # 204 No Content
    response.set_cookie('sid', '', secure=True, httponly=True, expires=0)

    return response

@bp.route('/get_login_token')
def get_login_token():
    response = {'token': generate_csrf_token()}
    db.session.commit()
    return response

def unauthorized_handler_json(error):
    return {
            'success': False,
            'reason': 'unauthorized'
            }, 401


api_unauthorized = bp.errorhandler(werkzeug.exceptions.Unauthorized)(unauthorized_handler_json)
