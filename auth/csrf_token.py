from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from secrets import token_urlsafe
from database import db

def generate_csrf_token():
    for try_ in range(3):
        try:
            csrf_token = token_urlsafe(64)
            sql = text('INSERT INTO CSRF_TOKEN VALUES (:user_token)').\
                    bindparams(user_token=csrf_token)
            db.session.execute(sql)
            return csrf_token
        except IntegrityError:
            pass

    raise RuntimeError

def check_csrf_token(csrf_token):
    sql = text('SELECT token from CSRF_TOKEN WHERE token=:user_token').\
            bindparams(user_token=csrf_token)
    token = db.session.execute(sql).scalar()

    if token is None:
        return False
    else:
        sql = text('DELETE FROM CSRF_TOKEN WHERE token=:user_token').\
            bindparams(user_token=csrf_token)
        db.session.execute(sql)
        return True
