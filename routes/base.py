from pkg.authlib.auth import db
from routes import auth_required
from flask import render_template


@auth_required
def root():
    """
    Description:
    :return:
    """
    return render_template("home.html")


@auth_required
def user_profile(username: str = None):
    """
    Description: Route to the profile of a user.
    :return: The selected user profile if it exists
    """
    if username:
        user = db.users.find_one({"username": username})
        if user:
            return render_template("profile.html", user_infos=user)
        return render_template("404.html")

    return render_template("profile.html")
