import base64

from pkg.authlib import db
from routes import auth_required
from flask import render_template, request, session


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
        av = request.files["file"]
        db.users.update_one(
            {"username": session.get("username")},
            {"$set": {"avatar": av.read()}}
        )

    if username:
        user = db.users.find_one({"username": username})
        if user:
            if user.get("avatar", None):
                avatar = f"data:image/png;charset=utf-8;base64,{base64.b64encode(user['avatar']).decode('utf-8')}"
            else:
                avatar = None
            return render_template("profile.html", user_infos=user, avatar=avatar)
        return render_template("404.html")

    return render_template("404.html")
