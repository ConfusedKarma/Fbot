import pyrogram

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os

from config import Config
from pyrogram import Client 
logging.getLogger("pyrogram").setLevel(logging.WARNING)

class fbot(Client):
    
    def __init__(self):
        super().__init__(
            session_name="FBOT",
            bot_token = Config.TOKEN,
            api_id = Config.APP_ID,
            api_hash = Config.API_HASH,
            workers = 20,
            plugins = dict(
                root="plugins"
            )
        )

if __name__ == "__main__" :
    fbot().run()
