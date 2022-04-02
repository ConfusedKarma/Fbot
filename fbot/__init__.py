import os

# the logging things
import logging

from fbot.sample_config import Config


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


LOGGER = logging.getLogger(__name__)
BOT_TOKEN = Config.BOT_TOKEN
APP_ID = Config.APP_ID
API_HASH = Config.API_HASH
CUSTOM_CMD = Config.CUSTOM_CMD
