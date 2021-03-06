from pyrogram import Client, filters
from fbot import fbot, AUTH_USERS, TO_CHANNEL
from fbot.sample_config import Config
#a = [594813047] # add user ids as list
#b = -1001142186094 # add the chat id

#@fbot.on_message(filters.chat(a))
#async def fwd(fbot, message):
    #await message.forward(b)




@Client.on_message(filters.chat(Config.AUTH_USERS) & ~filters.command(["start", "help"]))
async def autopost(bot, update):
    if (AUTH_USERS) == 0 or (TO_CHANNEL) == 0 or update.chat.id not in AUTH_USERS:
        return
    try:
        for chat_id in TO_CHANNEL:
                await update.forward(chat_id=chat_id)
    except Exception as error:
        print(error)
