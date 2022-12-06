from pkg.authlib.auth import db
from routes import auth_required
from flask import render_template, request, session


@auth_required
def root():
    """
    Description:

    :return:
    """
    if request.method == "POST":
        promo = session.get("promo")

    return render_template("home.html")


@auth_required
def user_profile(username: str):
    """
    Description: Route to the profile of a user.

    :param username: User profile provided in url
    :return: The selected user profile if it exists
    """
    if request.method == "POST":
        pass
        # avatar upload function

    if username:
        user = db.users.find_one({"username": username})
        if user:
            return render_template("profile.html", user_infos=user)
        return render_template("404.html")

    return render_template("404.html")
