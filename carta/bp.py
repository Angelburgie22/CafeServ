from flask import Blueprint
from auth.auth import active_session_decorator as active_session
import werkzeug.exceptions

bp = Blueprint('api_carta', __name__, url_prefix='/api/carta')

def unauthorized_handler_json(error):
    return {
            'success': False,
            'reason': 'unauthorized'
            }, 401


api_unauthorized = bp.errorhandler(werkzeug.exceptions.Unauthorized)(unauthorized_handler_json)

