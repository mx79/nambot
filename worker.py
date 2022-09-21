import os
import json
from typing import Dict
from app import publisher, subscriber
from pkg.bot.nlu import IntentClassifier, EntityExtractor
from pkg.bot.conversation import Transcript, Conversation

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# =================================================== FUNCTIONS =================================================== #


def transform(user_id: str, msg: str) -> Transcript:
    """
    Description: The function that get intent from redis message and return a dict with infos
    :param user_id: The name of the channel used (user id)
    :param msg: The content of the message published on Redis
    :return: A dict with some information
    """
    conv = Conversation(user_id)
    for c in conv_list.values():
        if c.conv_id == user_id:
            conv = c
    intent = cls.get_intent(msg)
    entities = ext.get_entity(msg)
    transcript = Transcript(user_id, msg, intent, entities)
    conv.add_transcript(transcript)
    conv_list[user_id] = conv
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


# =================================================== VARIABLES =================================================== #

# Instantiate a classifier with the model we want
cls = IntentClassifier("base_keras.pkl")

# Instantiate an entity extractor
ext = EntityExtractor("regex.json")

# Dict of all conversation
conv_list = dict()

# Listen to all channels matching the pattern below
subscriber.psubscribe(**{"ongoing_conversation_*": primary_handler})

print("============================================================"
      " Ready to process "
      "============================================================")

# =================================================== LAUNCH =================================================== #

# Launch of the worker
if __name__ == "__main__":
    subscriber.run_in_thread()
