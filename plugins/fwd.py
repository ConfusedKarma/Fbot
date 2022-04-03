from pyrogram import filters
from Fbot import fbot
from config import CHANNEL_ID, AUTH_USERS

#a = [594813047] # add user ids as list
#b = -1001142186094 # add the chat id of channel

@fbot.on_message(filters.chat(AUTH_USERS))
async def fwd(fbot, message):
    await message.forward(Config.CHANNEL)
