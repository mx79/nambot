import flask
from app import cache
from flask import render_template
from routes import no_auth_required


@no_auth_required
@cache.cached(timeout=50)
def forgot_password():
    """
    Description:
    :return:
    """
    if flask.request.method == "GET":
        return render_template("forgot.html")
    # Form where user can post email in order to
    # send email with link to reset pwd
