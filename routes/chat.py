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
    for doc in db.users.find():
        if doc["username"] == current_id:
            promo = doc["promo"]
    return
