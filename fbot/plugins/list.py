from pyrogram import Client, filters
from time import sleep, time
from fbot import fbot, CUSTOM_CMD


@Client.on_message(filters.command("adminlist", CUSTOM_CMD))
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


@Client.on_message(filters.command("botlist", CUSTOM_CMD))
def bot_list(fbot, message):
    sleep(0.1)
    chat_type = message.chat.type
    if chat_type != "private":
        bots = ""
        for i in fbot.get_chat_members(message.chat.id, filter="bots"):
            bots += " 🤖 -> @{}\n".format(i.user.username)
        message.reply(f'Bot list:\n{bots}', parse_mode="Markdown", disable_web_page_preview=True)
