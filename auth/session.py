from flask import Blueprint, request, Response, make_response, abort
import werkzeug.exceptions
from .csrf_token import check_csrf_token
from .auth import create_session, close_session, get_active_session, active_session_decorator as active_session
from database import db

bp = Blueprint('api_session', __name__, url_prefix='/api/session')

@bp.route('/create', methods=['POST'])
def create():
    if not request.json:
        abort(400)
    if any(not isinstance(request.json[i], str) for i in ('user', 'passwd', 'token')):
        abort(400)

    user = request.json['user']
    passwd = request.json['passwd']
    csrf_token = request.json['token']

    with db.session() as session:
        if not check_csrf_token(csrf_token):
            session.commit()
            return {'success': False, 'reason':'Invalid login request token'}, 400

        user_session = create_session(user, passwd)
        if user_session is None:
            session.commit()
            return {'success': False, 'reason':'Invalid credentials'}, 401

        session.commit()

    username, token = user_session

    response = make_response({'success':True, 'identifier':'cookies'})
    response.set_cookie('user', secure=True, httponly=True, value=username)
    response.set_cookie('sid', secure=True, httponly=True, value=token)

    return response

@bp.route('/close', methods=['DELETE'])
@active_session
def close():
    response = Response(status=204) # 204 No Content

    user, sid = get_active_session()
    close_session(user, sid)

    return response

@bp.errorhandler(werkzeug.exceptions.Unauthorized)
def api_unauthorized(error):
    return {
            'success': False,
            'reason': 'unauthorized'
            }, 401


