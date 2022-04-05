import httpx
from fbot import CUSTOM_CMD
from pyrogram import Client, filters
from pyrogram.types import Message

timeout = httpx.Timeout(40, pool=None)

http = httpx.AsyncClient(http2=True, timeout=timeout)


@Client.on_message(filters.command("paste", CUSTOM_CMD))
async def nekobin(c: Client, m: Message):
    if m.reply_to_message:
        if m.reply_to_message.document:
            tfile = m.reply_to_message
            to_file = await tfile.download()
            with open(to_file, "rb") as fd:
                mean = fd.read().decode("UTF-8")
        if m.reply_to_message.text:
            mean = m.reply_to_message.text

        url = "https://nekobin.com/api/documents"
        r = await http.post(url, json={"content": mean})
        await m.reply_text(url, disable_web_page_preview=True)
    else:
        await m.reply_text("Reply to Document or Text File")
