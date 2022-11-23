from flask import render_template, request, session
from pkg.authlib.auth import db
from routes import auth_required


@auth_required
def chat_receiver():
    """
    Description:
    :return:
    """
    if request.method == "POST":
        promo = session.get("promo")

    return render_template("chat.html")
