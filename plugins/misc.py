import os
import io
import sys
import traceback
from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime
from platform import python_version
from pyrogram import __version__

import asyncio

import humanize

from Fbot import fbot

CUSTOM_CMD = "!"
START_TIME = datetime.now()

@Client.on_message(filters.command("up", CUSTOM_CMD))
async def up(bot, message):
    txt = (
        f"-> Current Uptime: `{str(datetime.now() - START_TIME).split('.')[0]}`\n"
        f"-> Python: `{python_version()}`\n"
        f"-> Pyrogram: `{__version__}`"
    )
    await message.reply(txt)



@Client.on_message(filters.command("id", CUSTOM_CMD))
async def get_id(bot, message):
    msg = message.reply_to_message or message
    out_str = f"**Chat ID** : `{(msg.forward_from_chat or msg.chat).id}`\n"
    out_str += f"**Message ID** : `{msg.forward_from_message_id or msg.message_id}`\n"
    if msg.from_user:
        out_str += f"**From User ID** : `{msg.from_user.id}`\n"
    if msg.sender_chat:
        out_str += f"**Channel ID** : `{msg.sender_chat.id}`\n"
    file_id = None
    if msg.audio:
        type_ = "audio"
        file_id = msg.audio.file_id
    elif msg.animation:
        type_ = "animation"
        file_id = msg.animation.file_id
    elif msg.document:
        type_ = "document"
        file_id = msg.document.file_id
    elif msg.photo:
        type_ = "photo"
        file_id = msg.photo.file_id
    elif msg.sticker:
        type_ = "sticker"
        file_id = msg.sticker.file_id
    elif msg.voice:
        type_ = "voice"
        file_id = msg.voice.file_id
    elif msg.video_note:
        type_ = "video_note"
        file_id = msg.video_note.file_id
    elif msg.video:
        type_ = "video"
        file_id = msg.video.file_id
    if file_id is not None:
        out_str += f"💾**Media Type:** `{type_}`\n"
        out_str += f"🗃️**File ID:** `{file_id}`"
    await message.reply(out_str)

async def progress_callback(current, total, fbot, message: Message):
    if int((current / total) * 100) % 25 == 0:
        await message.edit(f"{humanize.naturalsize(current)} / {humanize.naturalsize(total)}")


@Client.on_message(filters.command("upload", CUSTOM_CMD))
async def upload(fbot, message):
    if len(message.command) > 1:
        await fbot.send_document('self', message.command[1], progress=progress_callback, progress_args=(fbot, message))
    else:
        await message.reply('No path provided.')
        await asyncio.sleep(3)

    await message.delete()
