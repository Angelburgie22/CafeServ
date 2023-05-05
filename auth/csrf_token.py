from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from secrets import token_urlsafe
from database import db
from models import CSRF_Token

def generate_csrf_token():
    for try_ in range(3):
        try:
            with db.session.begin_nested() as nested:
                csrf_token = token_urlsafe(48)
                db.session.add(CSRF_Token(token=csrf_token))
                nested.commit()
                return csrf_token
        except IntegrityError:
            pass

    raise RuntimeError('CSRF token not unique')

def check_csrf_token(csrf_token):
    if len(csrf_token) != 64:
        return False
    token = db.session.execute(delete(CSRF_Token)\
                .filter(CSRF_Token.token == csrf_token)\
                .returning(CSRF_Token.token)
                ).one_or_none()

    return token is not None

