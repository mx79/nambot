import redis
from os import getenv
from datetime import timedelta

# ======================== CONFIG OF FLASK APP ========================= #

# Global
SECRET_KEY = getenv('SECRET_KEY')

# Flask-Session
SESSION_TYPE = getenv('SESSION_TYPE')
SESSION_REDIS = redis.from_url(getenv('REDIS_URL'))
PERMANENT_SESSION_LIFETIME = timedelta(hours=int(getenv('PERMANENT_SESSION_LIFETIME')))
