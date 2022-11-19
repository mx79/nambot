from flask import Flask
from flask_caching import Cache
from routes.home import root
from routes.bugs import bugs
from routes.features import features
from routes.forgot import forgot_password
from routes.login import login
from routes.logout import logout
from routes.chatbot import chatbot_receiver
from routes.chat import chat_receiver

# Flask app init
app = Flask(__name__)
cache = Cache(config={'CACHE_TYPE': 'simple'})
app.config.from_pyfile("./config/config.py")

# TODO: Discussion de groupe avec Redis
# TODO: Email verification
# TODO: Email forgot password process
# TODO: Uppercase first letter of entity "VILLE"

# @app.before_request
# def make_session_permanent():

# Basic routes
app.add_url_rule("/", "root", root)
app.add_url_rule("/bugs", "bugs", bugs, methods=["GET", "POST"])
app.add_url_rule("/features", "features", features)

# Authentication
app.add_url_rule("/forgot-password", "forgot-password", forgot_password, methods=["GET", "POST"])
app.add_url_rule("/login", "login", login, methods=["GET", "POST"])
app.add_url_rule("/logout", "logout", logout)

# Chatting methods
app.add_url_rule("/chatbot-receiver", "chatbot_receiver", chatbot_receiver, methods=["POST"])
app.add_url_rule("/chat-receiver/{promo}", "chat_receiver", chat_receiver, methods=["GET", "POST"])


# Launch webserver
if __name__ == '__main__':
    cache.init_app(app)
