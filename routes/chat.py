from routes import auth_required
from flask import request, session


@auth_required
def chat_receiver():
    """
    Description:
    """
    if request.method == "POST":
        promo = session.get("promo")
