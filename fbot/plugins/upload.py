import asyncio

import humanize
from pyrogram import filters, Client
from pyrogram.types import Message

from fbot import CUSTOM_CMD, Config

async def progress_callback(current, total, bot: UserBot, message: Message):
    if int((current / total) * 100) % 25 == 0:
        await message.edit(f"{humanize.naturalsize(current)} / {humanize.naturalsize(total)}")




@Client.on_message(filters.command("upload", CUSTOM_CMD) & filters.user(Config.AUTH_USERS))
async def upload(bot, message: Message):
    if len(message.command) > 1:
        await bot.send_document('message.chat.id', message.command[1], progress=progress_callback, progress_args=(bot, message))
    else:
        await message.edit('No path provided.')
        await asyncio.sleep(3)

    await message.delete()
