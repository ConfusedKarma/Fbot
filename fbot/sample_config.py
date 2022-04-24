import os
from dotenv import load_dotenv


load_dotenv("config.env")

class Config(object):
      BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
      APP_ID = int(os.environ.get("APP_ID", 12345))
      API_HASH = os.environ.get("API_HASH")
      CUSTOM_CMD = os.environ.get("CUSTOM_CMD", "!")
      TO_CHANNEL = int(os.environ.get("TO_CHANNEL", ""))
      # Array to store users who are authorized to use the bot
      AUTH_USERS = list(
  set(
    int(x)
    for x in os.environ.get(
      "AUTH_USERS", ""
    ).split()
  )
)
      #download location
      DOWNLOAD_LOCATION = "./downloads"

class Production(Config):
    LOGGER = False


class Development(Config):
    LOGGER = True

