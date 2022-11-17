import flask
from flask import redirect, render_template, session


def forgot_password():
    """
    Description:
    :return:
    """
    if session.get("user_id") is not None:
        return redirect("/")
    if flask.request.method == "GET":
        return render_template("forgot.html")
    # Form where user can post email in order to
    # send email with link to reset pwd
