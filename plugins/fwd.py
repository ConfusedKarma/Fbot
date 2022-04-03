from pyrogram import Client, filters


a = [594813047] # add user ids as list
b = -1001193710741 # add the chat id of channel

@Client.on_message(filters.chats(a))
async def fwd(message):
    await message.forward(b)
