from routes import auth_required, no_auth_required, tmp_auth_required
from flask import redirect, render_template, request, session
from pkg.authlib.auth import db, create_user, send_email, verify_password, update_password, user_in_db


@no_auth_required
def login():
    """
    Description:
    :return:
    """
    session.permanent = True
    # Checking HTTP method used
    if request.method == "POST":
        # Login form data
        login_username = request.form.get("login_username", "")
        login_pwd = request.form.get("login_password", "")
        # Signup form data
        signup_username = request.form.get("signup_username", "")
        signup_promo = request.form.get("signup_promo", "")
        signup_email = request.form.get("signup_email", "")
        signup_pwd = request.form.get("signup_password", "")
        # Starting test tree for login form
        if login_username and login_pwd != "":
            for doc in db.users.find():
                if login_username == doc["username"] and verify_password(request.form['login_password'],
                                                                         doc["password"]):
                    user = db.users.find_one({"username": login_username})
                    session["username"] = login_username
                    session["promo"] = user["promo"]
                    session["email"] = user["email"]
                    return redirect("/")
            return render_template("login.html", pwd_validation="Nom d'utilisateur ou mot de passe invalide")
        # Starting test tree for signup form
        if signup_username and signup_email and signup_pwd != "":
            indb = user_in_db(signup_username, signup_email)
            if indb is None:
                # Create a temporary user while waiting for an email verification
                session["tmp_user"] = True
                create_user(signup_username, signup_promo, signup_email, signup_pwd, tmp=True)
                send_email(signup_email, option="verification")
                return render_template("email-verification.html")
            else:
                return render_template("login.html", msg=indb, card_back=True)

    return render_template("login.html")


@auth_required
def logout():
    """
    Description:
    :return:
    """
    session.pop("username", None)
    return render_template("logout.html")


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


@no_auth_required
def forgot_password(tmp_string: str = None):
    """
    Description:
    :param tmp_string:
    :return:
    """
    # Checking HTTP method used
    if request.method == "POST":
        if tmp_string is None:
            forgot_email = request.form.get("forgot_email", "")
            send_email(forgot_email, "forgot")
            return render_template("forgot.html", send=True)
        else:
            new_pwd = request.form.get("new_password")
            doc = db.tmp_forgot_url.find_one({"url": tmp_string})
            update_password(doc["email"], new_pwd)
            return render_template("forgot.html", pwd_changed=True, send=True)

    if tmp_string:
        if db.tmp_forgot_url.find_one({"url": tmp_string}):
            return render_template("forgot.html", arg=tmp_string)
        return render_template("404.html")

    return render_template("forgot.html")
