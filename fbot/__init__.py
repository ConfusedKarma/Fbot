# needed to appropriately, select ENV vars / Config vars
import os

# the logging things
import logging

from fbot.sample_config import Config


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


LOGGER = logging.getLogger(__name__)
APP_ID = Config.APP_ID
API_HASH = Config.API_HASH
BOT_TOKEN = Config.BOT_TOKEN
CUSTOM_CMD = Config.CUSTOM_CMD
AUTH_USERS = list(Config.AUTH_USERS)
AUTH_USERS = list(set(AUTH_USERS))
TO_CHANNEL = list(Config.TO_CHANNEL)
DOWNLOAD_LOCATION = Config.DOWNLOAD_LOCATION
# create download directory, if not exist
if not os.path.isdir(DOWNLOAD_LOCATION):
    os.makedirs(DOWNLOAD_LOCATION)

help_message = []
