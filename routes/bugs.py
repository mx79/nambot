from routes import auth_required, cache
from flask import render_template


@auth_required
@cache.cached(timeout=50)
def bugs():
    """
    Description: Shows bugs template where you can post a bug about the app
    :return: render_template bugs.html if authenticated
    """
    return render_template("bugs.html")
