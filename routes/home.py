from routes import auth_required
from flask import redirect, render_template, session, url_for


@auth_required
def root():
    """
    Description:
    :return:
    """
    return render_template("home.html")
