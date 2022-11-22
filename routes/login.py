from routes import no_auth_required
from flask import redirect, render_template, request, session
from pkg.authlib.auth import db, create_user, send_email, verify_password, user_in_db


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
                    session["user_id"] = login_username
                    return redirect("/")
            return render_template("login.html", pwd_validation="Nom d'utilisateur ou mot de passe invalide")
        # Starting test tree for signup form
        if signup_username and signup_email and signup_pwd != "":
            indb = user_in_db(signup_username, signup_email)
            if indb is None:
                # Create a temporary user while waiting for an email verification
                session["tmp_user"] = True
                create_user(signup_username, signup_promo,  signup_email, signup_pwd, tmp=True)
                send_email(signup_email, option="verification")
                return render_template("email-verification.html")
            else:
                return render_template("login.html", msg=indb, card_back=True)

    return render_template("login.html")
