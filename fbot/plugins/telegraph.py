from pyrogram import Client, filters
from pyrogram.types import Message
from telegraph import upload_file
from fbot import CUSTOM_CMD


@Client.on_message(filters.command("tlg", CUSTOM_CMD) & ~filters.edited)
async def telegraph(c: Client, m: Message, strings):
    if m.reply_to_message:
        if (
            m.reply_to_message.photo
            or m.reply_to_message.video
            or m.reply_to_message.animation
        ):
            d_file = await m.reply_to_message.download()
            media_urls = upload_file(d_file)
            tele_link = "https://telegra.ph" + media_urls[0]
            await m.reply_text(tele_link)
    else:
        await m.reply_text("Reply?")
