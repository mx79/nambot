from routes import auth_required


@auth_required
def user_profile(username):
    """
    Description: Route to the profile of a user.
    :return: The selected user profile if it exists
    """
