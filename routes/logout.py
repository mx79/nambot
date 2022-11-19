from routes import auth_required
from flask import render_template, session


@auth_required
def logout():
    """
    Description:
    :return:
    """
    session.pop("user_id", None)
    return render_template("logout.html")
