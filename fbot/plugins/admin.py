import asyncio
import time
from emoji import get_emoji_regexp

from fbot import CUSTOM_CMD

from pyrogram import Client, filters
from pyrogram.types import ChatPermissions, Message
from pyrogram.errors import (UsernameInvalid,
                            ChatAdminRequired,
                            PeerIdInvalid,
                            UserIdInvalid)


async def admin_check(message: Message) -> bool:
    client = message._client
    chat_id = message.chat.id
    user_id = message.from_user.id

    check_status = await client.get_chat_member(
        chat_id=chat_id,
        user_id=user_id
    )
    admin_strings = [
        "creator",
        "administrator"
    ]
    return check_status.status in admin_strings



# Mute permissions
mute_permission = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_other_messages=False,
    can_add_web_page_previews=False,
    can_send_polls=False,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False
)

# Unmute permissions
unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True,
    can_send_polls=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False
)

@Client.on_message(filters.command("unpin", CUSTOM_CMD))
async def unpin_message(client, message):
    if message.chat.type in ['group', 'supergroup']:
        chat_id = message.chat.id
        can_pin = await admin_check(message)
        if can_pin:
            try:
                await client.unpin_chat_message(
                    chat_id
                )
            except UsernameInvalid:
                await message.reply("`Invalid username`")
                return

            except PeerIdInvalid:
                await message.reply("`Invalid username or userid`")
                return

            except UserIdInvalid:
                await message.reply("`Invalid userid`")
                return

            except ChatAdminRequired:
                await message.reply("`Permission denied`")
                return

            except Exception as e:
                await message.reply("`Error!`\n"
                            f"**Log:** `{e}`"
                        )
                return
        else:
            await message.reply("`Permission denied`")
    else:
        await message.delete()


@Client.on_message(filters.command("pin", CUSTOM_CMD))
async def pin_message(client, message):
    if message.chat.type in ['group', 'supergroup']:
        chat_id = message.chat.id
        can_pin = await admin_check(message)
        if can_pin:
            try:
                if message.reply_to_message:
                    disable_notification = True
                    if len(message.command) >= 2 and message.command[1] in ['alert', 'notify', 'loud']:
                        disable_notification = False
                    await client.pin_chat_message(
                        chat_id,
                        message.reply_to_message.message_id,
                        disable_notification=disable_notification
                    )
            except UsernameInvalid:
                await message.reply("`Invalid username`")
                return

            except PeerIdInvalid:
                await message.reply("`Invalid username or userid`")
                return

            except UserIdInvalid:
                await message.reply("`Invalid userid`")
                return

            except ChatAdminRequired:
                await message.reply("`Permission denied`")
                return

            except Exception as e:
                await message.reply("`Error!`\n"
                            f"**Log:** `{e}`"
                        )
                return
        else:
            await message.reply("`Permission denied`")
    else:
        await message.delete()


@Client.on_message(filters.command("mute", CUSTOM_CMD))
async def mute_hammer(client, message):
    if message.chat.type in ['group', 'supergroup']:
        chat_id = message.chat.id
        can_mute = await admin_check(message)
        if can_mute:
            try:
                if message.reply_to_message:
                    user_id = message.reply_to_message.from_user.id
                else:
                    usr = await client.get_users(message.command[1])
                    user_id = usr.id
            except IndexError:
                await message.reply('some ooga booga')
                return
            try:
                get_mem = await client.get_chat_member(
                        chat_id,
                        user_id
                        )
                await client.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=user_id,
                    permissions=mute_permission
                )
                await message.reply(
                    f"[{get_mem.user.first_name}](tg://user?id={get_mem.user.id}) **Muted Indefinitely**")
            except Exception as e:
                await message.reply("`Error!`\n"
                        f"**Log:** `{e}`"
                    )
                return
        else:
            await message.reply("`permission denied`")
    else:
        await message.delete()


@Client.on_message(filters.command("unmute", CUSTOM_CMD))
async def unmute(client, message):
    if message.chat.type in ['group', 'supergroup']:
        chat_id = message.chat.id
        can_unmute = await admin_check(message)
        if can_unmute:
            try:
                if message.reply_to_message:
                    user_id = message.reply_to_message.from_user.id
                else:
                    usr = await client.get_users(message.command[1])
                    user_id = usr.id
            except IndexError:
                await message.reply('some ooga booga')
                return
            try:
                get_mem = await client.get_chat_member(
                        chat_id,
                        user_id
                        )
                await client.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=user_id,
                    permissions=unmute_permissions
                )
                await message.reply(
                        f"[{get_mem.user.first_name}](tg://user?id={get_mem.user.id}) **Unmuted**"
                        )
            except ChatAdminRequired:
                await message.reply("`permission denied`")
                return
            except Exception as e:
                await message.reply("`Error!`\n"
                        f"**Log:** `{e}`"
                    )
                return
    else:
        await message.delete()


@Client.on_message(filters.command("kick", CUSTOM_CMD))
async def kick_user(client, message):
    if message.chat.type in ['group', 'supergroup']:
        chat_id = message.chat.id
        can_kick = await admin_check(message)
        if can_kick:
            try:
                if message.reply_to_message:
                    user_id = message.reply_to_message.from_user.id
                else:
                    usr = await client.get_users(message.command[1])
                    user_id = usr.id
            except IndexError:
                await message.reply('some ooga booga')
                return
            try:
                get_mem = await client.get_chat_member(
                    chat_id,
                    user_id
                    )
                await client.kick_chat_member(chat_id, get_mem.user.id, int(time.time() + 45))
                await message.reply(
                    f"[{get_mem.user.first_name}](tg://user?id={get_mem.user.id}) **Kicked**"
                    )
            except ChatAdminRequired:
                await message.reply("`permission denied`")
                return
            except Exception as e:
                await message.reply("`Error!`\n"
                    f"**Log:** `{e}`"
                )
                return
        else:
            await message.reply("`permission denied`")
    else:
        await message.delete()


@Client.on_message(filters.command("ban", CUSTOM_CMD))
async def ban_usr(client, message):
    if message.chat.type in ['group', 'supergroup']:
        chat_id = message.chat.id
        can_ban = await admin_check(message)

        if can_ban:
            try:
                if message.reply_to_message:
                    user_id = message.reply_to_message.from_user.id
                else:
                    usr = await client.get_users(message.command[1])
                    user_id = usr.id
            except IndexError:
                await message.reply('some ooga booga')
                return
            if user_id:
                try:
                    get_mem = await client.get_chat_member(chat_id, user_id)
                    await client.kick_chat_member(chat_id, user_id)
                    await message.reply(
                        f"[{get_mem.user.first_name}](tg://user?id={get_mem.user.id}) **Banned**\n")

                except UsernameInvalid:
                    await message.reply("`Invalid username`")
                    return

                except PeerIdInvalid:
                    await message.reply("`Invalid username or userid`")
                    return

                except UserIdInvalid:
                    await message.reply("`Invalid userid`")
                    return

                except ChatAdminRequired:
                    await message.reply("`Permission denied`")
                    return

                except Exception as e:
                    await message.reply(f"**Log:** `{e}`")
                    return

        else:
            await message.reply("`permission denied`")
            return
    else:
        await message.delete()


@Client.on_message(filters.command("unban", CUSTOM_CMD))
async def unban_usr(client, message):
    if message.chat.type in ['group', 'supergroup']:
        chat_id = message.chat.id
        can_unban = await admin_check(message)
        if can_unban:
            try:
                if message.reply_to_message:
                    user_id = message.reply_to_message.from_user.id
                else:
                    usr = await client.get_users(message.command[1])
                    user_id = usr.id
            except IndexError:
                await message.reply('some ooga booga')
                return
            try:
                get_mem = await client.get_chat_member(
                    chat_id,
                    user_id
                    )
                await client.unban_chat_member(chat_id, get_mem.user.id)
                await message.reply(
                    f"[{get_mem.user.first_name}](tg://user?id={get_mem.user.id}) **Unbanned**\n"
                    )
            except UsernameInvalid:
                await message.reply("`Invalid username`")
                return

            except PeerIdInvalid:
                await message.reply("`Invalid username or userid`")
                return

            except UserIdInvalid:
                await message.reply("`Invalid userid`")
                return

            except ChatAdminRequired:
                await message.reply("`Permission denied`")
                return

            except Exception as e:
                await message.reply(f"**Log:** `{e}`")
                return
    else:
        await message.delete()


@Client.on_message(filters.command("promote", CUSTOM_CMD))
async def promote_usr(client, message):
    if message.chat.type in ['group', 'supergroup']:
        cmd = message.command
        custom_rank = ""
        chat_id = message.chat.id
        can_promo = await admin_check(message)

        if can_promo:
            try:
                if message.reply_to_message:
                    user_id = message.reply_to_message.from_user.id
                    custom_rank = get_emoji_regexp().sub(u'', " ".join(cmd[1:]))
                else:
                    usr = await client.get_users(message.command[1])
                    custom_rank = get_emoji_regexp().sub(u'', " ".join(cmd[2:]))
                    user_id = usr.id
            except IndexError:
                await message.reply('some ooga booga')
                return
            get_mem = await client.get_chat_member(
                        chat_id,
                        user_id
                        )
            if len(custom_rank) > 15:
                custom_rank = custom_rank[:15]


        if user_id:
            try:
                await client.promote_chat_member(chat_id, user_id,
                                                can_change_info=True,
                                                can_delete_messages=True,
                                                can_restrict_members=True,
                                                can_invite_users=True,
                                                can_pin_messages=True)
                await client.set_administrator_title(chat_id, user_id, custom_rank)
                await message.reply(f"**Promoted** [{get_mem.user.first_name}](tg://user?id={get_mem.user.id})")

            except UsernameInvalid:
                await message.reply("`Invalid username`")
                return
            except PeerIdInvalid:
                await message.reply("`Invalid username or userid`")
                return
            except UserIdInvalid:
                await message.reply("`Invalid userid`")
                return

            except ChatAdminRequired:
                await message.reply("`Permission denied`")
                return
            except Exception as e:
                await message.reply(f"**Log:** `{e}`")
                return
    else:
        await message.delete()


@Client.on_message(filters.command("demote", CUSTOM_CMD))
async def demote_usr(client, message):
    if message.chat.type in ['group', 'supergroup']:
        chat_id = message.chat.id
        can_demote = await admin_check(message)

        if can_demote:
            try:
                if message.reply_to_message:
                    user_id = message.reply_to_message.from_user.id
                else:
                    usr = await client.get_users(message.command[1])
                    user_id = usr.id
            except IndexError:
                await message.reply('some ooga booga')
                return
            try:
                get_mem = await client.get_chat_member(
                    chat_id,
                    user_id
                    )
                await client.promote_chat_member(chat_id, get_mem.user.id,
                                                can_change_info=False,
                                                can_delete_messages=False,
                                                can_restrict_members=False,
                                                can_invite_users=False,
                                                can_pin_messages=False)
                await message.reply(f"**Demoted** [{get_mem.user.first_name}](tg://user?id={get_mem.user.id})")
            except ChatAdminRequired:
                await message.reply("`Permission denied`")
                return

            except Exception as e:
                await message.reply(f"**Log:** `{e}`")
                return
    else:
        await message.delete()


@Client.on_message(filters.command("invitelink", CUSTOM_CMD))
async def invite_link(client, message):
    if message.chat.type in ["group", "supergroup"]:
        can_invite = await admin_check(message)
        if can_invite:
            try:
                link = await client.export_chat_invite_link(message.chat.id)
                await message.reply(text=link)
            except Exception as e:
                print(e)
                await message.reply("`Permission denied`")
    else:
        await message.delete()
