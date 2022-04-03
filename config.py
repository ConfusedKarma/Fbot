import os

class Config(object):
      TOKEN = os.environ.get("BOT_TOKEN", "")
      APP_ID = int(os.environ.get("APP_ID", 12345))
      API_HASH = os.environ.get("API_HASH")
      CHANNEL_ID = list(x for x in os.environ.get("CHANNEL_ID", "").replace("\n", " ").split(' '))
      AUTH_USERS = set()

if os.path.exists('auth_users.txt'):
    with open('auth_users.txt', 'r+') as f:
        lines = f.readlines()
        for line in lines:
            AUTH_USERS.add(int(line.split()[0]))
