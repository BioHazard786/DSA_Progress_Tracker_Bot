from os import getenv
from time import time
from dotenv import load_dotenv

try:
    load_dotenv("config.env")
except:
    pass


# * Telegram Credentials
class TeleConf(object):
    SESSION_NAME = str(
        getenv("SESSION_NAME", "DSA-Progress-Tracker-Bot")
    )  # ? Bot Session Name
    API_ID = int(getenv("API_ID"))
    API_HASH = str(getenv("API_HASH"))
    BOT_TOKEN = str(getenv("BOT_TOKEN"))
    BOT_START_TIME = time()
    BOT_USERNAME = ""
    OWNER_ID = int(getenv("OWNER_ID", "798171690"))


class MongoConf(object):
    MONGO_URL = str(getenv("MONGO_URL"))  # ? MongoDB URL
    MONGO_DB_NAME = str(getenv("MONGO_DB_NAME", "DSA-Bot"))  # ? MongoDB Database Name
