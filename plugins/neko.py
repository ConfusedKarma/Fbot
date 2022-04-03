import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message

SCHEMA = "https"
BASE = "nekobin.com"
ENDPOINT = f"{SCHEMA}://{BASE}/api/documents"
ANSWER = "**Long message from** {}\n{}"
TIMEOUT = 3
MESSAGE_ID_DIFF = 100
CUSTOM_CMD = "!"


@Client.on_message(filters.command("paste", CUSTOM_CMD))
async def neko(_, message: Message):
    """Paste very long code"""
    reply = message.reply_to_message

    if not reply:
        return

    # Ignore messages that are too old
    if message.message_id - reply.message_id > MESSAGE_ID_DIFF:
        return

    async with aiohttp.ClientSession() as session:
        async with session.post(
            ENDPOINT,
            json={"content": reply.text},
            timeout=TIMEOUT
        ) as response:
            key = (await response.json())["result"]["key"]

    await message.reply(reply, ANSWER.format(reply.from_user.mention, f"{BASE}/{key}.py"))

