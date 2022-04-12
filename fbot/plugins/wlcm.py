import asyncio
from asyncio import sleep
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from fbot.sample_config import Config

WELCOME_CHANNEL = Config.TO_CHANNEL

JOIN_TEXT = """Hello {} Welcome to Chat"""

BUTTONS = InlineKeyboardMarkup([[InlineKeyboardButton('Bot Owner', url='https://telegram.me/refundisillegal')]])


@Client.on_message(filters.chat(WELCOME_CHANNEL) & filters.new_chat_members)
async def welcome(client, message):
    if message.from_user.is_bot:
        await chat.kick_member(message.from_user.id)
    else:
        await message.reply_text(
        text=JOIN_TEXT.format(message.from_user.mention),
        reply_markup=BUTTONS,
        disable_web_page_preview=True,
        quote=True
    )
        await asyncio.sleep(60)
        await message.delete()
