from requests import post, get
from nksama import bot
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

CUSTOM_CMD = "!"

def paste(text):
    url = "https://spaceb.in/api/v1/documents/"
    res = post(url, data={"content": text, "extension": "txt"})
    return f"https://spaceb.in/{res.json()['payload']['id']}"


@Client.on_message(filters.command("start", CUSTOM_CMD)
def pastex(message):
    text = message.reply_to_message
    if text:
        x = paste(text.text)
        message.reply(x,
                      reply_markup=InlineKeyboardMarkup(
                          [[InlineKeyboardButton("Open", url=x)]]),
                      disable_web_page_preview=True)

    else:
        message.reply_text("Reply to a message!")
