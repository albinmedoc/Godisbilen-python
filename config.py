import os
from datetime import time
from dotenv import load_dotenv

class Config(object):
    load_dotenv()
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "SECRET_KEY"
    FLASK_DEBUG=1

    # How long does the van stay at each stop (seconds)
    STOP_TIME = 480

    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
    GOOGLE_ANALYTICS_TRACK_ID = os.getenv("GOOGLE_ANALYTICS_TRACK_ID")

    #Mail
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    OPENING_HOURS = {
        "4": [[time(20), time(23, 59, 59, 59)]],
        "5": [[time(0), time(4)], [time(20), time(23, 59, 59, 59)]],
        "6": [[time(0), time(4)], [time(20), time(23, 59, 59, 59)]]
    }

    #Database
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    