import flask
from flask import render_template, request
from routes import no_auth_required
from pkg.authlib.auth import send_email


@no_auth_required
def forgot_password():
    """
    Description:
    :return:
    """
    # Checking HTTP method used
    if flask.request.method == "POST":
        forgot_email = request.form.get("forgot_email", "")
        send_email(forgot_email, "forgot")
        return render_template("forgot.html", send=True)

    return render_template("forgot.html")
