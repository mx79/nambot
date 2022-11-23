import json
from typing import Dict
from routes import auth_required
from flask import request, session
from routes import cls, ext, publisher, subscriber, translator
from pkg.bot.conversation import Transcript, Conversation


def transform(username: str, msg: str) -> Transcript:
    """
    Description: The function that get intent from redis message and return a dict with infos
    :param username: The name of the channel used (user id)
    :param msg: The content of the message published on Redis
    :return: A dict with some information
    """
    conv = Conversation(username)
    for c in conv_list.values():
        if c.conv_id == username:
            conv = c
    intent = cls.get_intent(msg)
    entities = ext.get_entity(msg)
    transcript = Transcript(username, msg, intent, entities)
    conv.add_transcript(transcript)
    conv_list[username] = conv
    return transcript


def primary_handler(message: Dict):
    """
    Description: The function that first processes the message retrieved from the Redis channel
    :param message: Redis incoming message
    """
    user = message["channel"].replace("ongoing_conversation_", "")
    data = message["data"]
    res = transform(user, data).as_dict()
    publisher.publish("ongoing_infos_" + user,
                      f'{json.dumps(eval(str(res)))!s}')


# Dict of all conversation
conv_list = dict()

# Listen to all channels matching the pattern below
subscriber.psubscribe(**{"ongoing_conversation_*": primary_handler})

# Run redis in thread
subscriber.run_in_thread()


@auth_required
def chatbot_receiver():
    """
    Description: Endpoint waiting to receive user message from frontend.
    Once message is received, publish on the right redis channel.
    Then get response on another redis channel.
    Finally, post the Nambot response to the frontend.
    :return: Nambot response's
    """
    # Subscribe to incoming bot response
    subscriber.subscribe("ongoing_infos_" + session.get("username"))
    # Get user message
    user_msg = request.get_json()["message"]
    detected_lang = translator.detect(user_msg).lang
    if detected_lang != "fr":
        msg_fr = translator.translate(user_msg, dest="fr").text
        publisher.publish("ongoing_conversation_" + session.get("username"), msg_fr)
        # Listen to redis worker response
        for i in subscriber.listen():
            message = json.loads(i["data"])
            try:
                new_msg = {"response": translator.translate(message["infos"]["response"], dest=detected_lang).text}
                return new_msg
            # TODO: Changer la langue du tts en fonction de la langue détectée
            except TypeError:
                return message["infos"]
    publisher.publish("ongoing_conversation_" + session.get("username"), user_msg)
    # Listen to redis worker response
    for i in subscriber.listen():
        message = json.loads(i["data"])
        return message["infos"]
