import httpx
from fbot import CUSTOM_CMD, AUTH_USERS
from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime
from fbot.sample_config import Config

timeout = httpx.Timeout(40, pool=None)

http = httpx.AsyncClient(http2=True, timeout=timeout)


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
        url = f"https://hastebin.com/{r.json()['key']}"
        end = datetime.now()
        ms = (end - start).seconds
        await m.reply_text("[HASTEBIN]({}) in\n{} seconds".format(url, ms, disable_web_page_preview=True))
    else:
        await m.reply_text("Reply to Document or Text File")


from requests import post, get
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def paste(text):
    url = "https://spaceb.in/api/v1/documents/"
    res = post(url, data={"content": text, "extension": "txt"})
    return f"https://spaceb.in/{res.json()['payload']['id']}"


@Client.on_message(filters.command("pst", CUSTOM_CMD) & filters.user(Config.AUTH_USERS) & ~filters.edited)
def pastex(_, message):
    text = message.reply_to_message
    if text:
        x = paste(text.text)
        message.reply(x,
                      reply_markup=InlineKeyboardMarkup(
                          [[InlineKeyboardButton("Open", url=x)]]),
                      disable_web_page_preview=True)

    else:
        message.reply_text("Reply to a message!")
