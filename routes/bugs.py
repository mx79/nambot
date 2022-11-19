from routes import auth_required
from flask import render_template


@auth_required
def bugs():
    """
    Description: Shows bugs template where you can post a bug about the app
    :return: render_template bugs.html if authenticated
    """
    return render_template("bugs.html")
