import os
import json
import redis
import flask
from os import getenv
from config import env
from googletrans import Translator
from flask import Flask, redirect, render_template, request, session, url_for
from pkg.authlib.auth import db, user_in_db, verify_password, create_user


# TODO: Discussion de groupe avec Redis
# TODO: Email verification
# TODO: Email forgot password process
# TODO: STT integration in js
# TODO: Uppercase first letter of entity "VILLE"


def redis_init() -> redis.client.Redis:
    """
    Description: Redis config initialization
    """
    # REDIS_URL = "redis://:@localhost:6379"
    REDIS_URL = getenv("REDIS_URL")
    redis_splitted_url = REDIS_URL.replace("@", " ").replace(":", " ").split(" ")
    redis_pwd = redis_splitted_url[2]
    redis_host = redis_splitted_url[3]
    redis_port = redis_splitted_url[4]
    return redis.Redis(
        host=redis_host,
        port=int(redis_port),
        password=redis_pwd,
        ssl=bool(os.getenv('REDIS_TLS')),
        ssl_cert_reqs=None,
        charset='utf-8',
        decode_responses=True
    )


# App init
env.verify()
app = Flask(__name__)
app.config.from_pyfile("./config/config.py")
publisher = redis_init()
subscriber = publisher.pubsub(ignore_subscribe_messages=True)
translator = Translator()


# @app.before_request
# def make_session_permanent():


@app.route('/')
def root():
    """
    Description:
    :return:
    """
    if session.get("user_id") is None:
        return redirect(url_for("login"))
    return render_template("home.html")


@app.route("/features")
def features():
    """
    Description:
    :return:
    """
    return render_template("features.html")


@app.route("/bugs")
def bugs():
    """
    Description:
    :return:
    """
    if session.get("user_id") is None:
        return redirect(url_for("login"))
    return render_template("bugs.html")


@app.route('/login', methods=["GET", "POST"])
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


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    """
    Description:
    :return:
    """
    if session.get("user_id") is not None:
        return redirect("/")
    if flask.request.method == "GET":
        return render_template("forgot.html")
    # Form where user can post email in order to
    # send email with link to reset pwd


@app.route('/logout')
def logout():
    """
    Description:
    :return:
    """
    if session.get("user_id") is None:
        return redirect(url_for("login"))
    session.pop("user_id", None)
    return render_template("logout.html")


@app.route("/chatbot-receiver", methods=["POST"])
def chatbot_receiver():
    """
    Description: Endpoint waiting to receive user message from frontend.
    Once message is received, publish on the right redis channel.
    Then get response on another redis channel.
    Finally, post the Nambot response to the frontend.
    :return: Nambot response's
    """
    # Subscribe to incoming bot response
    subscriber.subscribe("ongoing_infos_" + session.get("user_id"))
    # Get user message
    user_msg = request.get_json()["message"]
    detected_lang = translator.detect(user_msg).lang
    if detected_lang != "fr":
        msg_fr = translator.translate(user_msg, dest="fr").text
        publisher.publish("ongoing_conversation_" + session.get("user_id"), msg_fr)
        # Listen to redis worker response
        for i in subscriber.listen():
            message = json.loads(i["data"])
            try:
                new_msg = {"response": translator.translate(message["infos"]["response"], dest=detected_lang).text}
                return new_msg
            # TODO: Changer la langue du tts en fonction de la langue détectée
            except TypeError:
                return message["infos"]
    else:
        publisher.publish("ongoing_conversation_" + session.get("user_id"), user_msg)
        # Listen to redis worker response
        for i in subscriber.listen():
            message = json.loads(i["data"])
            return message["infos"]


@app.route('/chat-receiver/{promo}', methods=["GET", "POST"])
def chat_receiver():
    """
    Description:
    :return:
    """
    current_id = session.get("user_id")
    for doc in db.users.find():
        if doc["username"] == current_id:
            promo = doc["promo"]
    return


if __name__ == '__main__':
    app.run()
