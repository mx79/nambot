from flask import Flask, render_template
from routes.home import root
from routes.bugs import bugs
from routes.features import features
from routes.forgot import forgot_password
from routes.login import login
from routes.logout import logout
from routes.chatbot import chatbot_receiver
from routes.chat import chat_receiver
from routes.email_verif import email_verification
from routes.profile import user_profile

# Flask app init
app = Flask(__name__)
app.config.from_pyfile("./config/config.py")

# TODO: Email verification, manque le lien à envoyer et l'activation du compte gmail avec smtp
# TODO: Regroup some routes to reduce the quantity of .py files
# TODO: Ajouter des textes aux pages concernées
# TODO: Uppercase first letter of entity "VILLE"
# TODO: Discussion de groupe avec Redis
# TODO: Ajouter nos liens Linkedin en dessous de nos avatars


# ============================================= CUSTOM HANDLERS ============================================= #


@app.errorhandler(404)
def page_not_found(error):
    """
    Description: Handle ``error 404 not found``
    :return: Custom template of error 404
    """
    return render_template("404.html")


# @app.before_request
# def make_session_permanent():


# ============================================= ROUTES ============================================= #


# Basic routes
app.add_url_rule("/", view_func=root)
app.add_url_rule("/bugs", view_func=bugs, methods=["GET", "POST"])
app.add_url_rule("/features", view_func=features)
app.add_url_rule("/profile/<username>", view_func=user_profile)

# Authentication
app.add_url_rule("/forgot-password", view_func=forgot_password, methods=["GET", "POST"])
app.add_url_rule("/forgot-password/<tmp_string>", view_func=forgot_password, methods=["GET", "POST"])
app.add_url_rule("/email-verification", view_func=email_verification)
app.add_url_rule("/email-verified/<tmp_string>", view_func=email_verification)
app.add_url_rule("/login", view_func=login, methods=["GET", "POST"])
app.add_url_rule("/logout", view_func=logout)

# Chatting methods
app.add_url_rule("/chatbot-receiver", view_func=chatbot_receiver, methods=["POST"])
app.add_url_rule("/chat-receiver", view_func=chat_receiver, methods=["POST"])


# Launch webserver
if __name__ == '__main__':
    app.run()
