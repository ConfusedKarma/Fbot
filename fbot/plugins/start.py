from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from fbot import CUSTOM_CMD


START_TEXT = """Hello {} #fkoff"""

BUTTONS = InlineKeyboardMarkup([[InlineKeyboardButton('Owner', url='https://telegram.me/refundisillegal')]])



@Client.on_message(filters.command("start", CUSTOM_CMD))
async def start(bot, update):
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        reply_markup=BUTTONS,
        disable_web_page_preview=True,
        quote=True
    )
