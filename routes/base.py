import base64

from pkg.authlib import db
from routes import auth_required
from flask import render_template, request, session

# ============================================= HANDLERS ============================================= #


@auth_required
def root():
    """Route of the home only for authenticated users.

    :return: The home.html template if user is authenticated
    """
    return render_template("home.html")


@auth_required
def user_profile(username: str):
    """Route to the profile of a user only for authenticated users.

    :param username: User profile provided in url
    :return: The selected user profile if it exists
    """
    if request.method == "POST":
        avatar = request.files["file"]
        db.users.update_one(
            {"username": session.get("username")},
            {"$set": {"avatar": avatar.read()}}
        )

    if username:
        docs = list(db.users.find())
        for doc in docs:
            if doc["username"] == username:
                if doc.get("avatar", None):
                    avatar = f"data:image/*;charset=utf-8;base64,{base64.b64encode(doc['avatar']).decode('utf-8')}"
                else:
                    avatar = None
                return render_template("profile.html", user_infos=doc, avatar=avatar,
                                       users=[u["username"] for u in docs if
                                              u["username"] != username])
        return render_template("404.html")

    return render_template("404.html")
