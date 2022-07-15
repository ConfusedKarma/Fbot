import os
import asyncio
import io
import sys
import traceback
from pyrogram import Client, filters
from pyrogram.types import Message, User
from fbot.sample_config import Config

from pyrogram.raw import functions
from pyrogram.errors import PeerIdInvalid
from datetime import datetime
from time import sleep
import requests

from platform import python_version
from pyrogram import __version__

from fbot import fbot, CUSTOM_CMD


def ReplyCheck(message: Message):
    reply_id = None

    if message.reply_to_message:
        reply_id = message.reply_to_message.message_id

    elif not message.from_user.is_self:
        reply_id = message.message_id

    return reply_id



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
async def get_id(fbot, message):
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

@Client.on_message(filters.command("reverse", CUSTOM_CMD))
async def text_reverse(fbot, message: Message):
    cmd = message.command

    reverse_text = ""
    if len(cmd) > 1:
        reverse_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        reverse_text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.reply("`Give me something to reverse`"[::-1])
        await asyncio.sleep(2)
        await message.delete()
        return

    await message.reply(reverse_text[::-1])





WHOIS = (
    '**"{full_name}"**\n'
    "[Link to profile](tg://user?id={user_id})\n"
    "════════════════\n"
    "UserID: `{user_id}`\n"
    "First Name: `{first_name}`\n"
    "Last Name: `{last_name}`\n"
    "Username: `{username}`\n"
    "Last Online: `{last_online}`\n"
    "════════════════\n"
    "Bio:\n{bio}"
)

WHOIS_PIC = (
    '**"{full_name}"**\n'
    "[Link to profile](tg://user?id={user_id})\n"
    "════════════════\n"
    "UserID: `{user_id}`\n"
    "First Name: `{first_name}`\n"
    "Last Name: `{last_name}`\n"
    "Username: `{username}`\n"
    "Last Online: `{last_online}`\n"
    "════════════════\n"
    "Profile Pics: `{profile_pics}`\n"
    "Last Updated: `{profile_pic_update}`\n"
    "════════════════\n"
    "Bio:\n{bio}"
)


def LastOnline(user: User):
    if user.is_bot:
        return ""
    elif user.status == "recently":
        return "Recently"
    elif user.status == "within_week":
        return "Within the last week"
    elif user.status == "within_month":
        return "Within the last month"
    elif user.status == "long_time_ago":
        return "A long time ago :("
    elif user.status == "online":
        return "Currently Online"
    elif user.status == "offline":
        return datetime.fromtimestamp(user.last_online_date).strftime(
            "%a, %d %b %Y, %H:%M:%S"
        )



def FullName(user: User):
    return user.first_name + " " + user.last_name if user.last_name else user.first_name


def ProfilePicUpdate(user_pic):
    return datetime.fromtimestamp(user_pic[0].date).strftime("%d.%m.%Y, %H:%M:%S")



@Client.on_message(filters.command("wh", CUSTOM_CMD))
async def who_is(fbot, message: Message):
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif message.reply_to_message and len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except ValueError:
            pass
    try:
        user = await fbot.get_users(get_user)
    except PeerIdInvalid:
        await message.reply("I don't know that User.")
        await asyncio.sleep(2)
        await message.delete()
        return

    user_details = await fbot.get_chat(get_user)
    bio = user_details.bio
    user_pic = await fbot.get_profile_photos(user.id)
    pic_count = await fbot.get_profile_photos_count(user.id)

    if not user.photo:
        await message.reply(
            WHOIS.format(
                full_name=FullName(user),
                user_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name if user.last_name else "",
                username=user.username if user.username else "",
                last_online=LastOnline(user),
                bio=bio if bio else "`No bio set up.`",
            ),
            disable_web_page_preview=True,
        )
    elif user.photo:
        await fbot.send_photo(
            message.chat.id,
            user_pic[0].file_id,
            caption=WHOIS_PIC.format(
                full_name=FullName(user),
                user_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name if user.last_name else "",
                username=user.username if user.username else "",
                last_online=LastOnline(user),
                profile_pics=pic_count,
                bio=bio if bio else "`No bio set up.`",
                profile_pic_update=ProfilePicUpdate(user_pic),
            ),
            reply_to_message_id=ReplyCheck(message),
        )

        await message.delete()

@Client.on_message(filters.command("ping", CUSTOM_CMD))
async def ping(fbot, message: Message):
    start = datetime.now()
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await message.reply(f"**Pong!**\n`{ms} ms`")




from emoji import UNICODE_EMOJI




@Client.on_message(filters.command("uni", CUSTOM_CMD))
async def checks_unicode(_, message: Message):
    uni_msg = await message.reply("`Processing...`")
    r_msg = message.reply_to_message
    if not r_msg:
        return await uni_msg.edit("`Reply to a text message!`")
    msg_text = r_msg.text
    if not msg_text:
        return await uni_msg.edit("`Reply to a text message!`")
    # Checking if the message have unicode characters
    uni_count = 0
    for char in list(msg_text):
        try:
            char.encode("ascii")
        except:
            if char in UNICODE_EMOJI["en"]:
                return
            uni_count += 1
    if uni_count == 0:
        await uni_msg.edit("`Non-Unicode Characters are included in this message!`")
    else:
        await uni_msg.edit(f"`{uni_count} Unicode Characters are included in this message!`")


import urllib.request

from bs4 import BeautifulSoup

@Client.on_message(filters.command("cs", CUSTOM_CMD))
async def cs(_, message: Message):
    ok = await message.reply("`Processing...`")
    score_page = "http://static.cricinfo.com/rss/livescores.xml"
    page = urllib.request.urlopen(score_page)
    soup = BeautifulSoup(page, "html.parser")
    result = soup.find_all("description")
    Sed = ""
    for match in result:
        Sed += match.get_text() + "\n\n"
    await ok.edit(
        f"<b><u>Match information gathered successful</b></u>\n\n\n<code>{Sed}</code>",
        parse_mode="HTML",
    )


@Client.on_message(filters.command("csr", CUSTOM_CMD) & (filters.regex("https") | filters.regex("http") | filters.regex("www") & filters.private) & filters.user(Config.AUTH_USERS))
async def scrapping(bot, message):
    txt = await message.reply_text("Validating Link", quote=True)
    try:  # Extracting Raw Data From Webpage ( Unstructured format)
        url = str(message.text)
        request = requests.get(url)
        await txt.edit(text=f"Getting Raw Data from {url}", disable_web_page_preview=True)
        file_write = open(f'RawData-{message.chat.username}.txt', 'a+')
        file_write.write(f"{request.content}")  # Writing Raw Content to Txt file
        file_write.close()
        await message.reply_document(f"RawData-{message.chat.username}.txt", caption="©@BugHunterBots", quote=True)
        os.remove(f"RawData-{message.chat.username}.txt")
        await txt.delete()
    except Exception as error:
        print(error)
        await message.reply_text(text=f"{error}", disable_web_page_preview=True, quote=True)
        await txt.delete()
        return
    try:
        txt = await message.reply_text(text=f"Getting HTML code from {url}", disable_web_page_preview=True, quote=True)
        soup = BeautifulSoup(request.content, 'html5lib')  # Extracting Html code in Tree Format
        file_write = open(f'HtmlData-{message.chat.username}.txt', 'a+')
        soup.data = soup.prettify()  # parsing HTML
        file_write.write(f"{soup.data}")  # writing data to txt
        file_write.close()
        await message.reply_document(f"HtmlData-{message.chat.username}.txt", caption="©@BugHunterBots", quote=True)
        os.remove(f"HtmlData-{message.chat.username}.txt")
        await txt.delete()
    except Exception as error:
        await message.reply_text(text=f"{error}", disable_web_page_preview=True, quote=True)
        await txt.delete()
        return
    try:
        txt = await message.reply_text(f"Getting all Links from {url}", disable_web_page_preview=True, quote=True)
        file_write = open(f'AllLinks-{message.chat.username}.txt', 'a+')
        for link in soup.find_all('a'):  # getting all <a> tags in Html
            links = link.get('href')  # Extracting Href value of <a>
            file_write.write(f"{links}\n\n")  # writing links to txt file
        file_write.close()
        await message.reply_document(
            f"AllLinks-{message.chat.username}.txt",
            caption="©@SinghRobot"
        )
        os.remove(f"AllLinks-{message.chat.username}.txt")
        await txt.delete()
    except Exception as error:
        await message.reply_text(text=f"{error}", disable_web_page_preview=True, quote=True)
        await txt.delete()

    try:
        txt = await message.reply_text(
            f"Getting all Paragraph from {url} ...",
            disable_web_page_preview=True,
            quote=True
        )
        file_write = open(f'AllParagraph-{message.chat.username}.txt', 'a+')
        paragraph = ""
        for para in soup.find_all('p'):  # Extracting all <p> tags
            paragraph = para.get_text()  # Getting Text from Paragraphs
            file_write.write(f"{paragraph}\n\n")  # writing to a file
        file_write.close()
        
        await txt.delete()
        await message.reply_document(
            f"AllParagraph-{message.chat.username}.txt",
            caption="©@SinghRobot",
            quote=True
        )
        os.remove(f"AllParagraph-{message.chat.username}.txt")
    except Exception as error:
        await message.reply_text(text=f"No Paragraphs Found!!", disable_web_page_preview=True, quote=True)
        await txt.delete()
        return
