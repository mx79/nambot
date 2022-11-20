from flask import session
from routes import tmp_auth_required


@tmp_auth_required
def email_verification(tmp_string: str = None):
    """
    Description:
    """

    # Drop tmp_user key of user session when link is GET by HTTP method
    # session.pop("tmp_user", None)
