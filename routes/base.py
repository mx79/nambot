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
def bugs():
    """
    Description: Shows bugs template where you can post a bug about the app
    :return: render_template bugs.html if authenticated
    """
    return render_template("bugs.html")


def features():
    """
    Description:
    :return:
    """
    return render_template("features.html")


@auth_required
def user_profile(username):
    """
    Description: Route to the profile of a user.
    :return: The selected user profile if it exists
    """
