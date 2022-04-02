import os

class Config(object):
      TOKEN = os.environ.get("BOT_TOKEN", "")
      APP_ID = int(os.environ.get("APP_ID", 12345))
      API_HASH = os.environ.get("API_HASH")
      CHANNEL = list(x for x in os.environ.get("CHANNEL_ID", "").replace("\n", " ").split(' '))