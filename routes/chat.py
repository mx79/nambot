from flask import session
from pkg.authlib.auth import db
from routes import auth_required


@auth_required
def chat_receiver():
    """
    Description:
    :return:
    """
    current_id = session.get("user_id")
    doc = db.users.find_one({"username": current_id})
    if doc:
        promo = doc["promo"]
    return
