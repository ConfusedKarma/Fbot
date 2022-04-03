from pyrogram import Client, filters
from time import sleep, time
from Fbot import fbot


@Client.on_message(filters.command(['adminlist'], ['.', '!']))
def user_list(fbot, message):
    sleep(0.1)
    chat_type = message.chat.type
    if chat_type != "private":
        creator = ""
        admins = ""
        for i in fbot.get_chat_members(message.chat.id, filter="administrators"):
            if not i.user.is_bot:
                if i.status == "creator":
                    creator += "👑 -> @{}\n\n".format(i.user.username) if i.user.username \
                        else "👑 -> [{}](tg://user?id={})\n\n".format(
                            i.user.first_name, i.user.id
                        )
                if i.status == "administrator":
                    admins += " ⛑ -> @{}\n".format(i.user.username) if i.user.username \
                        else " ⛑ -> [{}](tg://user?id={})\n".format(
                            i.user.first_name, i.user.id
                        )
        message.reply(f'Admin list:\n{creator}{admins}', parse_mode="Markdown", disable_web_page_preview=True)


@Client.on_message(filters.command(['botlist'], ['.', '!']))
def bot_list(fbot, message):
    sleep(0.1)
    chat_type = message.chat.type
    if chat_type != "private":
        bots = ""
        for i in fbot.get_chat_members(message.chat.id, filter="bots"):
            bots += " 🤖 -> @{}\n".format(i.user.username)
        message.reply(f'Bot list:\n{bots}', parse_mode="Markdown", disable_web_page_preview=True)


@Client.on_message(filters.command(['ghostlist'], ['.', '!']))
def ghost_list(fbot, message):
    sleep(0.1)
    chat_type = message.chat.type
    if chat_type != "private":
        num = 0
        for i in fbot.iter_chat_members(message.chat.id):
            if i.user.is_deleted:
                num += 1
        message.reply(f'Deleted account number : {num}', disable_web_page_preview=True)


@Client.on_message(filters.command(['zombie'], ['.', '!']))
def zombie_list(fbot, message):
    sleep(0.1)
    chat_type = message.chat.type
    if chat_type != "private":
        num = 0
        for i in fbot.iter_chat_members(message.chat.id):
            if i.user.status in ("long_time_ago", "within_month"):
                num += 1
        message.reply(f'Zombie account number : {num}', disable_web_page_preview=True)


@Client.on_message(filters.command(['ghostkick'], ['.', '!']))
def ban_ghosts(fbot, message):
    sleep(0.1)
    chat_type = message.chat.type
    if fbot.get_chat_member(message.chat.id, fbot.get_me().id).status == "creator" or "administrator":
        if chat_type != "private":
            num = 0
            for i in fbot.iter_chat_members(message.chat.id):
                if i.user.is_deleted:
                    fbot.kick_chat_member(message.chat.id, i.user.id, time() + 60)
                    num += 1
                    sleep(0.1)
            message.reply(f'{num} deleted account is kicked')


@Client.on_message(filters.command(['zombiekick'], ['.', '!']))
def ban_zombies(fbot, message):
    sleep(0.1)
    chat_type = message.chat.type
    if fbot.get_chat_member(message.chat.id, fbot.get_me().id).status == "creator" or "administrator":
        if chat_type != "private":
            num = 0
            for i in fbot.iter_chat_members(message.chat.id):
                if i.user.status in ("long_time_ago", "within_month"):
                    fbot.kick_chat_member(message.chat.id, i.user.id, time() + 60)
                    num += 1
                    sleep(0.1)
            message.reply(f'{num} zombie account is kicked')
