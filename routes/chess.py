from routes import auth_required
from flask import render_template
from pkg.authlib.auth import db


@auth_required
def chess(tmp_string: str = None):
    """
    Description:

    :return:
    """
    if tmp_string:
        doc = db.tmp_chess_url.find_one({"url": tmp_string})
        if doc:
            return render_template("chess.html", arg=tmp_string)
        return render_template("404.html")

    return render_template("chess.html")
