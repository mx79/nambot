from flask import Flask, render_template
from flask_socketio import SocketIO
from routes.base import root, user_profile
from routes.auth import email_verification, forgot_password, login, logout
from routes.chatbot import chatbot_receiver

# Flask app init
app = Flask(__name__)
app.config.from_pyfile("./config/config.py")
socketio = SocketIO(app)


# TODO: Afficher les profils par username.
# TODO: Upload un avatar par utilisateur et le stocker dans le user correspondant.
# TODO: Essayer de réduire le thread cleaner avec un zip() sur les collections.

# TODO: Créer des parties d'échecs en invitant des utilisateurs.

# TODO: Discussion de groupe avec Redis.


# ============================================= CUSTOM HANDLERS ============================================= #


@app.errorhandler(404)
def page_not_found(error):
    """
    Handle `error 404 not found`.

    :return: Custom template of error 404
    """
    return render_template("404.html")


# @app.before_request
# def make_session_permanent():


# ============================================= ROUTES ============================================= #


# Basic routes
app.add_url_rule("/", view_func=root, methods=["GET", "POST"])
app.add_url_rule("/profile/<username>", view_func=user_profile, methods=["GET", "POST"])

# Authentication
app.add_url_rule("/forgot-password", view_func=forgot_password, methods=["GET", "POST"])
app.add_url_rule("/forgot-password/<tmp_string>", view_func=forgot_password, methods=["GET", "POST"])
app.add_url_rule("/email-verification", view_func=email_verification)
app.add_url_rule("/email-verified/<tmp_string>", view_func=email_verification)
app.add_url_rule("/login", view_func=login, methods=["GET", "POST"])
app.add_url_rule("/logout", view_func=logout)

# ChatBot
app.add_url_rule("/chatbot-receiver", view_func=chatbot_receiver, methods=["POST"])

# Jinja function


# Launch webserver
if __name__ == '__main__':
    socketio.run(app)
    # app.jinja_env.globals.update()
