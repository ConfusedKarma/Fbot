import asyncio
from functools import wraps
from pyrogram.types import Message

from Fbot import fbot


def admins_only(func):
    @wraps(func)
    async def decorator(bot: Fbot, message: Message):
        if bot.is_admin(message):
            await func(bot, message)

        await message.delete()

    decorator.admin = True

    return decorator
