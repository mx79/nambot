import os
import time
import redis
import threading
from os import getenv
from config import env
from functools import wraps
from pkg.authlib.auth import db
from googletrans import Translator
from flask import redirect, session, url_for
from pkg.bot.nlu import IntentClassifier, EntityExtractor

# Reducing the amount of log generated by Tensorflow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# App init
env.verify()


def clean_url():
    """
    Description: Deletes any temporary url than have more than 10 minutes of existence.
    This thread is run every 10 seconds.
    """
    threading.Timer(10.0, clean_url).start()
    print("Cleaning Temporary URL...")
    actual_time = int(time.time())
    for doc in db.tmp_email_validation_url.find():
        diff = actual_time - doc["created_at"]
        if diff >= 600:
            db.tmp_email_validation_url.delete_one({"created_at": doc["created_at"]})
    for doc in db.tmp_forgot_url.find():
        diff = actual_time - doc["created_at"]
        if diff >= 600:
            db.tmp_forgot_url.delete_one({"created_at": doc["created_at"]})


def redis_init() -> redis.client.Redis:
    """
    Description: Redis config initialization
    :return: An instance of Redis client
    """
    # Redis for session, cache and chatbot
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


def auth_required(func):
    """
    Description: Decorator implementing authentication system.
    It performs url blocking if the user is not connected.
    :return: wrapper func
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return wrapper


def no_auth_required(func):
    """
    Description: Decorator extending authentication system.
    It performs url blocking if the user is connected.
    :return: wrapper func
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("user_id") is not None:
            return redirect("/")
        return func(*args, **kwargs)

    return wrapper


# Redis
publisher = redis_init()
subscriber = publisher.pubsub(ignore_subscribe_messages=True)

# Translator object
translator = Translator()

# Instantiate a classifier with the model we want
cls = IntentClassifier("base_keras.pkl")

# Instantiate an entity extractor
ext = EntityExtractor("regex.json")

# Launch thread cleaning temporary url
clean_url()
