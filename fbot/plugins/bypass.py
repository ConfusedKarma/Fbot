import regex as re
import cloudscraper

from pyrogram import Client, filters
from fbot import CUSTOM_CMD, AUTH_USERS
from fbot.sample_config import Config



def mdis_k(urlx):
    scraper = cloudscraper.create_scraper(interpreter="nodejs", allow_brotli=False)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"
    }
    apix = f"http://x.egraph.workers.dev/?param={urlx}"
    response = scraper.get(apix, headers=headers)
    query = response.json()
    return query


def mdisk(url):
    check = re.findall(r"\bhttps?://.*mdisk\S+", url)
    if not check:
        textx = f"Invalid mdisk url"
        return textx
    else:
        try:
            fxl = url.split("/")
            urlx = fxl[-1]
            uhh = mdis_k(urlx)
            text = f'Title : {uhh["filename"]}\n\n{uhh["download"]}'
            return text
        except ValueError:
            textx = f"The content is deleted."
            return textx


@Client.on_message(filters.command("mdisk", CUSTOM_CMD) & filters.regex(r"https?://[^\s]+"))
async def mdik(bot, update):
    url = update.matches[0].group(0)
    bsdk = mdisk(url)
    message = await update.reply_text(
        text=bsdk, disable_web_page_preview=True, quote=True
    )
