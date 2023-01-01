import threading

from routes import auth_required, no_auth_required
from flask import redirect, render_template, request, session
from pkg.authlib import db, create_user, send_email, verify_password, update_password, user_in_db

# ============================================= HANDLERS ============================================= #


@no_auth_required
def login():
    """The authentication logic is stored in this function.

    :return: Login template related to the information entered in the form
    """
    session.permanent = True
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
                    session["username"] = login_username
                    session["email"] = doc["email"]
                    return redirect("/")
            return render_template("login.html", pwd_validation="Nom d'utilisateur ou mot de passe invalide")
        # Starting test tree for signup form
        if signup_username and signup_promo and signup_email and signup_pwd != "":
            if indb := user_in_db(signup_username, signup_email):
                return render_template("login.html", msg=indb, card_back=True)

            # Create a temporary user while waiting for an email verification
            create_user(signup_username, signup_promo, signup_email, signup_pwd, tmp=True)
            threading.Thread(target=lambda x: send_email(x, option="verification"), args=(signup_email,)).start()
            return render_template("email-verification.html")

    return render_template("login.html")


@auth_required
def logout():
    """Pop the username session information which leads to the disconnection of this user.

    :return: The logout template
    """
    session.pop("username", None)
    return render_template("logout.html")


@no_auth_required
def email_verification(tmp_string: str = None):
    """The email verification logic is stored in this function.

    :param tmp_string: The temporary URL given in the request
    :return: Email verified template or 404 error if tmp_string is not valid
    """
    if tmp_string:
        if doc := db.tmp_email_validation_url.find_one({"url": tmp_string}):
            # Drop tmp_user key of user session when link is GET by HTTP method
            user = db.tmp_users.find_one({"email": doc["email"]})
            create_user(
                user["username"],
                user["promo"],
                user["email"],
                user["password"]
            )
            db.tmp_email_validation_url.delete_one({"url": doc["url"]})
            db.tmp_users.delete_one({"email": doc["email"]})
            return render_template("email-verification.html", arg=tmp_string)
        return render_template("404.html")

    return render_template("404.html")


@no_auth_required
def forgot_password(tmp_string: str = None):
    """The password forgetting process is stored in this function.

    :param tmp_string: The temporary URL given in the request
    :return: Forgot template or 404 error if tmp_string is not valid
    """
    if request.method == "POST":
        if tmp_string is None:
            forgot_email = request.form.get("forgot_email", "")
            if db.users.find_one({"email": forgot_email}):
                threading.Thread(target=lambda x: send_email(x, option="forgot"), args=(forgot_email,)).start()
                return render_template("forgot.html", send=True)
            return render_template("forgot.html", not_found=True)
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
