import flask
from routes import cache, no_auth_required
from pkg.authlib.auth import db, create_user, verify_password, user_in_db
from flask import redirect, render_template, session


@no_auth_required
@cache.cached(timeout=50)
def login():
    """
    Description:
    :return:
    """
    if session.get("user_id") is not None:
        return redirect("/")
    session.permanent = True
    # Basic render_template of login form page
    if flask.request.method == "GET":
        return render_template("login.html")
    # Login form data
    login_username = flask.request.form.get("login_username", "")
    login_pwd = flask.request.form.get("login_password", "")
    # Signup form data
    signup_username = flask.request.form.get("signup_username", "")
    signup_email = flask.request.form.get("signup_email", "")
    signup_promo = flask.request.form.get("signup_promo", "")
    signup_pwd = flask.request.form.get("signup_password", "")
    # Starting test tree for login form
    if login_username and login_pwd != "":
        for doc in db.users.find():
            if login_username == doc["username"] and verify_password(flask.request.form['login_password'],
                                                                     doc["password"]):
                session["user_id"] = login_username
                return redirect("/")
        return render_template("login.html", pwd_validation="Adresse email ou mot de passe invalide")
    # Starting test tree for signup form
    if signup_username and signup_email and signup_promo and signup_pwd != "":
        indb = user_in_db(signup_email)
        if indb is None:
            session["user_id"] = signup_username
            create_user(signup_username, signup_email, signup_promo, signup_pwd)
            # send_email_verif(signup_email)
            return redirect("/")
        else:
            return render_template("login.html", msg=indb, card_back=True)
