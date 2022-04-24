from pyrogram import Client, filters
from pyrogram.types import Message
from fbot import AUTH_USERS
from fbot.sample_config import Config



@Client.on_message(filters.command("dice", CUSTOM_CMD) & filters.user(Config.AUTH_USERS))
async def dice(c: Client, m: Message):
    dicen = await c.send_dice(
        m.chat.id,
        reply_to_message_id=m.message_id,
    )
    await dicen.reply_text
        ("result").format(
            number=dicen.dice.value,
        ),
        quote=True,
    )
