from .Fbot import fbot
from fbot import LOGGER
from pyrogram import __version__

if __name__ == "__main__":
    fbot().run()
    LOGGER.info(
            f"BOT RUNNING!"
            f"Pyrogram version - {__version__} "
        )
