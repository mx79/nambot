from pkg.authlib.auth import db, update_user
from routes import auth_required
from flask import render_template, request


@auth_required
def root():
    """
    Description:
    :return:
    """
    return render_template("home.html")


@auth_required
def user_profile(username: str, firstname: str = "", lastname: str = "", promo: str = ""):
    """
    Description: Route to the profile of a user.
    :return: The selected user profile if it exists
    :param username: User profile provided in url
    :param firstname: Updated firstname
    :param lastname: Updated lastname
    :param promo: Updated promo
    """

    if request.method == "POST":
        update_user(username, firstname, lastname, promo)

    if username:
        user = db.users.find_one({"username": username})
        if user:
            return render_template("profile.html", user_infos=user)
        return render_template("404.html")

    return render_template("404.html")
