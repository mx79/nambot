from flask import render_template, session
from routes import tmp_auth_required
from pkg.authlib.auth import db, create_user


@tmp_auth_required
def email_verification(tmp_string: str = None):
    """
    Description:
    :param tmp_string:
    :return:
    """
    if tmp_string:
        doc = db.tmp_email_validation_url.find_one({"url": tmp_string})
        if doc:
            # Drop tmp_user key of user session when link is GET by HTTP method
            session.pop("tmp_user", None)
            user = db.tmp_users.find_one({"email": doc["email"]})
            create_user(
                user["username"],
                user["promo"],
                user["email"],
                user["password"]
            )
            db.tmp_users.delete_one({"email": doc["email"]})
            return render_template("email-verification.html", arg=tmp_string)
    else:
        return render_template("email-verification.html")
