from routes import cache
from flask import render_template


@cache.cached(timeout=50)
def features():
    """
    Description:
    :return:
    """
    return render_template("features.html")
