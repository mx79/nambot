"""Flask configuration."""
import redis
from os import getenv
from datetime import timedelta

# ======== CONFIG OF FLASK APP ======== #

# Global
TESTING = True
DEBUG = True
FLASK_ENV = 'development'
SECRET_KEY = getenv('SECRET_KEY')

# Flask-Session
SESSION_TYPE = getenv('SESSION_TYPE')
SESSION_REDIS = redis.from_url(getenv('REDIS_URL'))
PERMANENT_SESSION_LIFETIME = timedelta(days=int(getenv('PERMANENT_SESSION_LIFETIME')))
