import re
from typing import Dict
from pkg.bot import bot_response
from flask import request, session
from routes import cls, ext
from routes import auth_required, bot_conversations


# ============================================= HANDLER ============================================= #


@auth_required
def chatbot_receiver() -> Dict[str, str]:
    """Endpoint waiting to receive user message from frontend.
    First, we process the user message with entities and intent.
    Then, we get the corresponding response from the ChatBot library in pkg/bot.
    Finally, we send Nambot response to the frontend.

    :return: Nambot response's
    """
    user = session.get("username")

    # Extract information from message
    msg = request.get_json()["message"]
    entities = ext.get_entity(f" {msg} ")
    intent = cls.get_intent(msg)

    # Check if there is a conv for this user
    if not bot_conversations.get(user, None):
        bot_conversations[user] = []
        resp = bot_response(entities, intent)
    else:
        previous_intent = bot_conversations[user][-1]
        resp = bot_response(entities, intent, previous_intent)

    # Append to conv dict the last intent detected
    bot_conversations[user].append(intent)

    return {"response": resp}
