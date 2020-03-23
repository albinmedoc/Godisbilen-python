import os
from datetime import time, date
from dotenv import load_dotenv

class Config(object):
    load_dotenv()
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "SECRET_KEY"
    FLASK_DEBUG=1

    # Time for the driver to jump in the van
    START_TIME = 600 # 10 min
    # The driver's starting position
    START_LOC = [55.639291, 13.096950]

    # How long does the van stay at each stop (seconds)
    STOP_TIME = 480 # 8 min

    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
    GOOGLE_ANALYTICS_TRACK_ID = os.getenv("GOOGLE_ANALYTICS_TRACK_ID")

    # Mail
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    # SMS
    SMS_USERNAME = os.getenv("SMS_USERNAME")
    SMS_USERID = os.getenv("SMS_USERID")
    SMS_HANDLE = os.getenv("SMS_HANDLE")

    INCLUDE_PHONE_NUMBER_ORDER = []

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Opening hours
    OPENING_HOURS = {
        "4": [[time(17), time(23)]], # Friday
        "5": [[time(15), time(23)]], # Saturday
        "6": [[time(17), time(21, 30)]] # Sunday
    }

    EXTRA_OPENING_HOURS = {
        # December
        date(2019, 12, 25): [[time(12), time(23, 59, 59, 59)]],
        date(2019, 12, 26): [[time(0), time(1)], [time(12), time(23, 59, 59, 59)]],
        date(2019, 12, 27): [[time(0), time(1)], [time(12), time(23, 59, 59, 59)]],
        date(2019, 12, 28): [[time(0), time(1)], [time(12), time(23, 59, 59, 59)]],
        date(2019, 12, 29): [[time(0), time(1)], [time(12), time(23, 59, 59, 59)]],
        date(2019, 12, 30): [[time(0), time(1)], [time(12), time(23, 59, 59, 59)]],
        date(2019, 12, 31): [[time(0), time(1)]],
        # January
        date(2020, 1, 1): [[time(12), time(23, 59, 59, 59)]],
        date(2020, 1, 2): [[time(0), time(1)], [time(12), time(23, 59, 59, 59)]],
        date(2020, 1, 3): [[time(0), time(1)], [time(12), time(23, 59, 59, 59)]],
        date(2020, 1, 4): [[time(0), time(1)], [time(12), time(23, 59, 59, 59)]],
        date(2020, 1, 5): [[time(0), time(1)], [time(12), time(23, 59, 59, 59)]],
        date(2020, 1, 6): [[time(0), time(1)], [time(12), time(23, 59, 59, 59)]],
        date(2020, 1, 7): [[time(0), time(1)]],
    }
    