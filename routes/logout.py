from routes import auth_required, cache
from flask import render_template, session


@auth_required
@cache.cached(timeout=50)
def logout():
    """
    Description:
    :return:
    """
    session.pop("user_id", None)
    return render_template("logout.html")
