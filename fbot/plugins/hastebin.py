import httpx
from fbot import CUSTOM_CMD, AUTH_USERS
from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime
from fbot.sample_config import Config

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

timeout = httpx.Timeout(40, pool=None)

http = httpx.AsyncClient(http2=True, timeout=timeout)


START_TEXT = """Hello {}\Click below button to open Paste-link"""

BUTTONS = InlineKeyboardMarkup([[InlineKeyboardButton('Paste-Link', url='purl')]])

@Client.on_message(filters.command("paste", CUSTOM_CMD) & filters.user(Config.AUTH_USERS) & ~filters.edited)
async def hastebin(c: Client, m: Message):
    start = datetime.now()
    if m.reply_to_message:
        if m.reply_to_message.document:
            tfile = m.reply_to_message
            to_file = await tfile.download()
            with open(to_file, "rb") as fd:
                mean = fd.read().decode("UTF-8")
        if m.reply_to_message.text:
            mean = m.reply_to_message.text

        url = "https://hastebin.com/documents"
        r = await http.post(url, data=mean.encode("UTF-8"))
        purl = f"https://hastebin.com/{r.json()['key']}"
        end = datetime.now()
        ms = (end - start).seconds
        #await m.reply_text("[HASTEBIN]({}) in\n{} seconds".format(purl, ms, disable_web_page_preview=True))
        await m.reply_text(
        text=START_TEXT.format(m.from_user.mention),
        reply_markup=BUTTONS,
        disable_web_page_preview=True,
        quote=True
    )
    else:
        await m.reply_text("Reply to Document or Text File")
