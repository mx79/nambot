import os
import time
import redis
import threading

from os import getenv
from config import env
from os.path import join
from functools import wraps
from pkg.authlib import db
from flask import redirect, session, url_for
from frtk import KerasIntentClassifier, RegexEntityExtractor

# ============================================= APP VAR ============================================= #

# App init
env.verify()

# Path to models
nlu_dir = join(os.getenv("BASE_DIR"), "resources", "data", "nlu.json")
regex_dir = join(os.getenv("BASE_DIR"), "resources", "data", "regex.json")

# Dict in memory containing all the chess games running at the moment
all_chess_games = {}

# Dict in memory containing the current conversation between the CnamBot and a user
bot_conversations = {}


# ============================================= THREADS ============================================= #


def clean_tmp():
    """Deletes any temporary url and temporary user that have more than 10 minutes of existence.
    This thread is run every 15 seconds.
    """
    threading.Timer(15.0, clean_tmp).start()
    actual_time = int(time.time())
    for doc in db.tmp_email_validation_url.find():
        diff = actual_time - doc["created_at"]
        if diff >= 600:
            db.tmp_email_validation_url.delete_one({"created_at": doc["created_at"]})
    for doc in db.tmp_forgot_url.find():
        diff = actual_time - doc["created_at"]
        if diff >= 600:
            db.tmp_forgot_url.delete_one({"created_at": doc["created_at"]})
    for doc in db.tmp_users.find():
        diff = actual_time - doc["created_at"]
        if diff >= 600:
            db.tmp_users.delete_one({"created_at": doc["created_at"]})


def clean_chess_url():
    """Deletes any temporary chess url that have more than 7 days of existence.
    This thread is run every 2 minutes.
    """
    threading.Timer(120.0, clean_chess_url).start()
    actual_time = int(time.time())
    for doc in db.tmp_chess_url.find():
        diff = actual_time - doc["created_at"]
        if diff >= 604800:
            db.tmp_chess_url.delete_one({"created_at": doc["created_at"]})


# ============================================= REDIS ============================================= #


def redis_init() -> redis.client.Redis:
    """Redis config initialization.

    :return: An instance of Redis client
    """
    # Redis for session, cache and chatbot
    redis_url = getenv("REDIS_URL")
    redis_splitted_url = redis_url.replace("@", " ").replace(":", " ").split(" ")
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


# ======================================= AUTHENTICATION DECORATORS ======================================= #


def auth_required(func):
    """Decorator for authentication system.
    It performs url blocking if the user is not connected.

    :return: Wrapper
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("username") is None:
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return wrapper


def no_auth_required(func):
    """Decorator for authentication system.
    It performs url blocking if the user is connected.

    :return: Wrapper
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("username") is not None:
            return redirect("/")
        return func(*args, **kwargs)

    return wrapper


# ======================================= APP VAR AND THREAD LAUNCH ======================================= #

# Redis
publisher = redis_init()
subscriber = publisher.pubsub(ignore_subscribe_messages=True)

# Instantiate a classifier with the model we want
cls = KerasIntentClassifier()
cls.train(nlu_dir)

# Instantiate an entity extractor
ext = RegexEntityExtractor(regex_dir)

# Launch threads responsible for the cleaning of temporary data
clean_tmp()
clean_chess_url()
