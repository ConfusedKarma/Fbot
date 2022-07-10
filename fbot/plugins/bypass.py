import regex as re
import cloudscraper

from pyrogram import Client, filters
from fbot import CUSTOM_CMD, AUTH_USERS
from fbot.sample_config import Config
import asyncio
from urllib.parse import urlparse
from bs4 import BeautifulSoup



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


@Client.on_message(filters.command("mdisk", CUSTOM_CMD) & filters.regex(r"https?://[^\s]+") & filters.user(Config.AUTH_USERS))
async def mdik(bot, update):
    url = update.matches[0].group(0)
    bsdk = mdisk(url)
    message = await update.reply_text(
        text=bsdk, disable_web_page_preview=True, quote=True
    )

async def get_link(url: str):
    client = cloudscraper.create_scraper(allow_brotli=False)
    p = urlparse(url)
    final_url = f'{p.scheme}://{p.netloc}/links/go'

    res = client.head(url)
    header_loc = res.headers['location']
    param = header_loc.split('postid=')[-1]
    req_url = f'{p.scheme}://{p.netloc}/{param}'

    p = urlparse(header_loc)
    ref_url = f'{p.scheme}://{p.netloc}/'

    h = { 'referer': ref_url }
    res = client.get(req_url, headers=h, allow_redirects=False)

    bs4 = BeautifulSoup(res.content, 'html.parser')
    inputs = bs4.find_all('input')
    data = { input.get('name'): input.get('value') for input in inputs }

    h = {
        'referer': ref_url,
        'x-requested-with': 'XMLHttpRequest',
    }
    asyncio.sleep(10)
    res = client.post(final_url, headers=h, data=data)
    try:
        return res.json()['url'].replace('\/','/')
    except Exception as e:
        print(e)
        return False


async def gp(message):
    if not message.text.startswith("https://gplinks") or message.text.startswith("gplinks"):
       await message.reply_text("Sorry, all I do is scrape GPLinks URLs :(")
       return
    m = await message.reply_text("Please wait...")
    link = await get_link(message.text)
    await m.delete()
    if not link:      
       await message.reply_text("Something went wrong\nTry again later..")
    else:
       await message.reply_text(f"Here is your direct link:\n\n{link}", disable_web_page_preview=True)
    
