import io
import sys
import traceback
from pyrogram import Client, filters
from datetime import datetime
from platform import python_version
from pyrogram import __version__


CUSTOM_CMD = "!"
START_TIME = datetime.now()

@Client.on_message(filters.command("up", CUSTOM_CMD))
async def up(_, message:):
    txt = (
        f"-> Current Uptime: `{str(datetime.now() - START_TIME).split('.')[0]}`\n"
        f"-> Python: `{python_version()}`\n"
        f"-> Pyrogram: `{__version__}`"
    )
    await message.reply(txt)
