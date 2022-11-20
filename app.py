from flask import Flask
from routes.home import root
from routes.bugs import bugs
from routes.features import features
from routes.forgot import forgot_password
from routes.login import login
from routes.logout import logout
from routes.chatbot import chatbot_receiver
from routes.chat import chat_receiver
from routes.email_verif import email_verification, generated_link
from routes.profile import user_profile

# Flask app init
app = Flask(__name__)
app.config.from_pyfile("./config/config.py")

# TODO: Email verification, manque le lien à envoyer et l'activation du compte gmail avec smtp
# TODO: Email forgot password process
# TODO: Regroup some routes to reduce the quantity of .py files
# TODO: Uppercase first letter of entity "VILLE"
# TODO: Discussion de groupe avec Redis

# @app.before_request
# def make_session_permanent():

# Basic routes
app.add_url_rule("/", "root", root)
app.add_url_rule("/bugs", "bugs", bugs, methods=["GET", "POST"])
app.add_url_rule("/features", "features", features)
app.add_url_rule("/profile/<username>", "profile", user_profile)

# Authentication
app.add_url_rule("/forgot-password", "forgot-password", forgot_password, methods=["GET", "POST"])
app.add_url_rule("/email-verification/<generated_string>", "email-verification", email_verification)
app.add_url_rule("/<generated_string>", "generated-link", generated_link)
app.add_url_rule("/login", "login", login, methods=["GET", "POST"])
app.add_url_rule("/logout", "logout", logout)

# Chatting methods
app.add_url_rule("/chatbot-receiver", "chatbot_receiver", chatbot_receiver, methods=["POST"])
app.add_url_rule("/chat-receiver/{promo}", "chat_receiver", chat_receiver, methods=["GET", "POST"])

# Launch webserver
if __name__ == '__main__':
    app.run()
