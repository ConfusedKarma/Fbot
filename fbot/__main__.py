import logging
from .fbot import fbot
from pyrogram import __version__

if __name__ == "__main__":
    fbot().run()
    fbot.loop.run_until_complete(main())
    logging.info(
            f"BOT RUNNING!"
)
    logging.info(
            f"Pyrogram version - {__version__} "
)
