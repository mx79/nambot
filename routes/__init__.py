from config import env
from functools import wraps
from flask import redirect, session, url_for

# App init
env.verify()


def auth_required(func):
    """
    Description: Decorator implementing authentication system.
    It performs url blocking if the user is not connected.
    :return: wrapper func
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper


def no_auth_required(func):
    """
    Description: Decorator extending authentication system.
    It performs url blocking if the user is connected.
    :return: wrapper func
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("user_id") is not None:
            return redirect("/")
        return func(*args, **kwargs)
    return wrapper
