from flask import request, abort
from database import db

def create_session(user:str, passwd:str) -> tuple[str, str] | None:
    return user, 'SID'

def close_session(user: str, token:str):
    pass

def check_session(user:str, sid):
    return True

def get_active_session():
    user = request.cookies.get('user', None)
    sid = request.cookies.get('sid', None)

    if user and sid:
        return user, sid
    else:
        return None

def active_session_decorator(func, handler=lambda *args, **kwargs:abort(401)):
    def wrapper(*args, **kwargs):
        user_session = get_active_session()

        if user_session and check_session(*user_session):
            return func(*args, **kwargs)
        else:
            return handler(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper

