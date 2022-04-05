from pyrogram import Client
from fbot import (
    APP_ID,
    API_HASH,
    BOT_TOKEN,
    DOWNLOAD_LOCATION
)

class fbot(Client):

    def __init__(self):
        name = self.__class__.__name__.lower()
        super().__init__(
            ":memory:",
            plugins=dict(root=f"{name}/plugins"),
            workdir=DOWNLOAD_LOCATION,
            api_id=APP_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            parse_mode="html",
            sleep_threshold=60,
        )
