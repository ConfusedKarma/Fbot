from pyrogram import Client, filters
from pyrogram.types.bots_and_keyboards.inline_keyboard_button import InlineKeyboardButton
from pyrogram.types.bots_and_keyboards.inline_keyboard_markup import InlineKeyboardMarkup
from pyrogram.types.messages_and_media import message

sudos = [594813047, 649998646, 90296554, 458802161]

def call_back_in_filter(data):
    return filters.create(
        lambda flt, _, query: flt.data in query.data,
        data=data
    )

def is_admin(group_id: int, user_id: int):
    try:
        user_data = client.get_chat_member(group_id, user_id)
        if user_data.status in ['administrator', 'creator']:
            # print(f'is admin user_data : {user_data}')
            return True
        else:
            # print('Not admin')
            return False
    except:
        # print('Not admin')
        return False


@Client.on_callback_query(call_back_in_filter("admin"))
def admeme_callback(_, client, query):
    scammer = query.data.split(":")[2]
    if is_admin(query.message.chat.id, query.from_user.id) and query.data.split(":")[1] == "unban":
        client.unban_chat_member(query.message.chat.id, scammer)
        query.answer('Unbanned!')
        query.message.edit(f'unbanned [{scammer}](tg://user?id={scammer})', parse_mode='markdown')
    else:
        message.reply('You are not admin!')


@Client.on_message(filters.command("ban", CUSTOM_CMD))
def ban(_, client, message):
    # scammer = reply.from_user.id
    reply = message.reply_to_message
    if is_admin(
            message.chat.id, message.from_user.id
    ) and message.from_user.id not in sudos and reply.from_user.id != 594813047:
        client.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        client.send_message(
            message.chat.id,
            f"Banned! {reply.from_user.username}",
            parse_mode="markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Unban",
                            callback_data=f"admin:unban:{message.reply_to_message.from_user.id}"
                        )
                    ],
                ]
            )
        )

    elif reply.from_user.id == 594813047:
        message.reply('This Person is my owner!')

    elif reply.from_user.id in sudos:
        message.reply("This Person is my sudo user !")

    elif message.from_user.id == 594813047 or message.from_user.id in sudos:
        client.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        client.send_message(
            message.chat.id,
            f"Banned! {reply.from_user.username}",
            parse_mode="markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Unban",
                            callback_data=f"admin:unban:{message.reply_to_message.from_user.id}"
                        )
                    ],
                ]
            )
        )
    else:
        message.reply('You are not admin')


@Client.on_message(filters.command("unban", CUSTOM_CMD))
def unban(_, client, message):
    try:
        user = message.text.split(" ")[1]
        if is_admin(message.chat.id, message.from_user.id):
            client.unban_chat_member(message.chat.id, user)
            message.reply('Unbanned!')
        if not is_admin(message.chat.id, message.from_user.id):
            message.reply("You aren't admin!")
        else:
            message.reply("I can't unban that uset")
    except Exception as e:
        message.reply(e)


@Client.on_message(filters.command("pin", CUSTOM_CMD))
def pin(_, client, message):
    if message.reply_to_message:
        message_id = message.reply_to_message.message_id
        if is_admin(message.chat.id, message.from_user.id):
            client.pin_chat_message(message.chat.id, message_id)

    elif not is_admin(message.chat.id, message.from_user.id):
        message.reply("You're not admin")
    elif not message.reply_to_message:
        message.reply("Reply to a message")
    else:
        message.reply("Make sure I'm admin and Can Pin Messages")


@Client.on_message(filters.command("unpin", CUSTOM_CMD))
def unpin(_, client, message):
    if message.reply_to_message:
        message_id = message.reply_to_message.message_id
        if is_admin(message.chat.id, message.from_user.id):
            client.unpin_chat_message(message.chat.id, message_id)
    elif not is_admin(message.chat.id, message.from_user.id):
        message.reply("You're not admin")
    elif not message.reply_to_message:
        message.reply("Reply to a message")
    else:
        message.reply("Make sure I'm admin and Can Pin Messages")


@Client.on_message(filters.command("kick", CUSTOM_CMD))
def kick(_, client, message):
    reply = message.reply_to_message
    if is_admin(message.chat.id, message.from_user.id) and reply:
        client.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        client.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        message.reply('kick @{} !'.format(message.reply_to_message.from_user.username))
    elif reply.from_user.id == 594813047:
        message.reply('This Person is my owner!')
    else:
        message.reply('You are not admin')


@Client.on_message(filters.command("promote", CUSTOM_CMD))
def promote(_, message):
    if is_admin(message.chat.id, message.from_user.id) and message.reply_to_message:
        message.chat.promote_member(message.reply_to_message.from_user.id)
        message.reply('Promoted @{} !'.format(message.reply_to_message.from_user.username))


@Client.on_message(filters.command("demote", CUSTOM_CMD))
def demote(_, message):
    if is_admin(message.chat.id, message.from_user.id) and message.reply_to_message:
        message.chat.promote_member(message.reply_to_message.from_user.id, False, False, False, False, False, False,
                                    False, False)
        message.reply('Demoted @{} !'.format(message.reply_to_message.from_user.username))

