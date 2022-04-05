import os
from dotenv import load_dotenv


load_dotenv("config.env")

class Config(object):
      BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
      APP_ID = int(os.environ.get("APP_ID", 12345))
      API_HASH = os.environ.get("API_HASH")
      CUSTOM_CMD = os.environ.get("CUSTOM_CMD", "!")
      CHANNEL_ID = list(x for x in os.environ.get("CHANNEL_ID", "").replace("\n", " ").split(' '))
      # Array to store users who are authorized to use the bot
      AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "").split())
      #download location
      DOWNLOAD_LOCATION = "./DOWNLOADS"
