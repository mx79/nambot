import time
from routes import auth_required
from flask import render_template, request, session
from pkg.authlib.auth import db, get_random_string


def create_chess_url(sender_email: str, receiver_email: str):
    """
    Description:

    :param sender_email:
    :param receiver_email:
    """
    db.tmp_chess_url.insert_one({
        "url": get_random_string(16),
        "created_at": int(time.time()),
        "sender_email": sender_email,
        "receiver_email": receiver_email
    })


@auth_required
def chess(tmp_string: str = None):
    """
    Description:

    :return:
    """
    if request.method == "POST":
        # Create a game
        receiver_email = request.form.get("", "")
        create_chess_url(session.get("email"), receiver_email)

    if tmp_string:
        doc = db.tmp_chess_url.find_one({"url": tmp_string})
        if doc:
            return render_template("chess.html", game_id=tmp_string)
        return render_template("404.html")

    return render_template("chess.html")
