from pyrogram import Client, filters
from fbot.sample_config import Config
from fbot import AUTH_USERS


users = Config.AUTH_USERS

@Client.on_message(filters.command(["start", "help"]))
async def start(bot, update):
    if update.from_user.id not in users:
        await bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id,
            revoke=True
        )
        return
