from pyrogram import filters
from fbot import fbot, AUTH_USERS, TO_CHANNEL

#a = [594813047] # add user ids as list
#b = -1001142186094 # add the chat id

#@fbot.on_message(filters.chat(a))
#async def fwd(fbot, message):
    #await message.forward(b)




@fbot.on_message(
    filters.chat & (
        filters.text |
        filters.audio |
        filters.document |
        filters.photo |
        filters.sticker |
        filters.video |
        filters.animation |
        filters.voice |
        filters.video_note |
        filters.contact |
        filters.location |
        filters.venue |
        filters.poll |
        filters.game
    )
)
async def autopost(bot, update):
    if len(AUTH_USERS) == 0 or len(TO_CHANNEL) == 0 or update.chat.id not in AUTH_USERS:
        return
    try:
        for chat_id in TO_CHANNEL:
                await update.forward(chat_id=chat_id)
    except Exception as error:
        print(error)
