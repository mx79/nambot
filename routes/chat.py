from routes import auth_required
from flask import request, session

# ============================================= HANDLER ============================================= #


@auth_required
def chat_receiver():
    """
    """
    if request.method == "POST":
        promo = session.get("promo")
