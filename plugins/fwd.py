from pyrogram import filters
from Fbot import fbot

a = [594813047] # add user ids as list
b = -1001193710741 # add the chat id of channel

@fbot.on_message(filters.chat(a))
async def fwd(message):
    await message.forward(b)
