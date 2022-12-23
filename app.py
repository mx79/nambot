from flask import Flask, render_template
from flask_socketio import SocketIO
from routes.chat import chat_receiver
from routes.base import root, user_profile
from routes.chatbot import chatbot_receiver
from routes.chess import chess_game, got_a_chess_move
from routes.auth import email_verification, forgot_password, login, logout

# Flask app init
app = Flask(__name__)
app.config.from_pyfile("./config/config.py")
socketio = SocketIO(app)


# TODO: Upload un avatar par utilisateur et le stocker dans le user correspondant.
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
app.add_url_rule("/email-verified/<tmp_string>", view_func=email_verification)
app.add_url_rule("/login", view_func=login, methods=["GET", "POST"])
app.add_url_rule("/logout", view_func=logout)

# Chat methods
app.add_url_rule("/chat-receiver", view_func=chat_receiver, methods=["POST"])
app.add_url_rule("/chatbot-receiver", view_func=chatbot_receiver, methods=["POST"])

# Chess
app.add_url_rule("/chess", view_func=chess_game, methods=["GET", "POST"])
app.add_url_rule("/chess/<tmp_string>", view_func=chess_game, methods=["GET", "POST"])
socketio.on_event("chess_move", got_a_chess_move, namespace="/chess")

# Launch webserver
if __name__ == '__main__':
    socketio.run(app)
