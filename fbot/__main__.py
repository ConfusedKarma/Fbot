import logging
from .fbot import fbot
from pyrogram import __version__

if __name__ == "__main__":
    fbot().run()
    logging.info(
            f"BOT RUNNING!"
)
    logging.info(
            f"Pyrogram version - {__version__} "
)
