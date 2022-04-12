import asyncio
from asyncio import sleep
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

WELCOME_CHANNEL = -1001193710741


@Client.on_message(filters.chat(WELCOME_CHANNEL) & filters.new_chat_members)
async def welcome(client, message):
    if message.from_user.is_bot:
        await chat.kick_member(message.from_user.id)
    else:
        await message.reply_text(" Hello {}, 🎉 Welcome to chat! 🎉", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="🔗  Join @ChuPeeps  🔗",url="t.me/ChuPeeps")],[InlineKeyboardButton(text="🚩  Bot Owner  🚩",url ="t.me/refundisillegal")]])).format(update.from_user.mention)
        await asyncio.sleep(60)
        await message.delete()
