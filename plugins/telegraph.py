from telegraph import upload_file
from pyrogram import Client, filters
from Fbot import fbot

CUSTOM_CMD = "!"

Client.on_message(filters.command("tlg", CUSTOM_CMD))
async def ul(_, message):
    reply = message.reply_to_message
    if reply.media:
        i = message.reply("**Downloading....**")
        path = reply.download()
        fk = upload_file(path)
        for x in fk:
            url = "https://telegra.ph" + x

        i.edit(f'Your telegraph [link]({url})', disable_web_page_preview=True)
