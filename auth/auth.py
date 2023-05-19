from flask import request, abort
from werkzeug.security import check_password_hash
from sqlalchemy import delete, func
from sqlalchemy.exc import IntegrityError
from secrets import token_urlsafe
from datetime import datetime, timedelta
from database import db
from models import UserAccount, UserSession, UserLoginInfo, CSRF_Token
import re

email_re = re.compile(r"([\w\d._+?!#$%&^'~|\/(){}=*-])+@(((?<=@)|\.)[\w\d]+){2,}")
username_re = re.compile(r'.{5,}')

dummy_passwd = 'pbkdf2:sha256:600000$9OmlyJr7wkbJqG3k$3620944e74d53d29edd2bf920faa19848a16584938639f10570748a7f5101951'


def create_user_session(user: str, passwd: str) -> UserSession | None:
    if email_re.fullmatch(user):
        identifier = UserAccount.email.ilike(user)
    elif username_re.fullmatch(user):
        identifier = UserAccount.username.ilike(user)
    else:
        return None

    user_id, login_info = db.session.query(UserAccount.id, UserLoginInfo)\
            .filter(identifier)\
            .filter(UserLoginInfo.account_id == UserAccount.id)\
            .one_or_none() or [None, None]

    if user_id is None or login_info is None:
        # Evita ataques de timing
        check_password_hash(dummy_passwd, passwd)
        return None

    passwd_hash = login_info.passwd_hash

    if not check_password_hash(passwd_hash, passwd):
        return None

    for i in range(3):
        try:
            with db.session.begin_nested() as nested:
                session_token = token_urlsafe(48)

                user_session = UserSession(id=session_token, account_id=user_id,
                                           expiration_time=datetime.now()+timedelta(weeks=1))

                db.session.add(user_session)
                nested.commit()

                return user_session

        except IntegrityError:
            pass

    raise RuntimeError(f'Error inserting session {session_token} into db')

def get_cookie_sid():
    return request.cookies.get('sid', None)

def get_active_session() -> UserSession:
    sid = get_cookie_sid()
    user_session = db.session.query(UserSession)\
            .filter(UserSession.expiration_time > func.now())\
            .filter(UserSession.id == sid).one()
    return user_session

def check_active_session() -> bool:
    sid = get_cookie_sid()
    return db.session.query(db.session.query(UserSession)\
            .filter(UserSession.expiration_time > func.now())\
            .filter(UserSession.id == sid).exists()).scalar()

def close_active_session():
    db.session.execute(delete(UserSession)\
            .filter(UserSession.id == get_cookie_sid()))

def active_session_decorator(func, handler=lambda *args, **kwargs:abort(401)):
    def wrapper(*args, **kwargs):
        user_sid = get_cookie_sid()

        if user_sid and check_active_session():
            return func(*args, **kwargs)
        else:
            return handler(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper

