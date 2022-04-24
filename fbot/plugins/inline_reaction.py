from typing import Dict, List
from fbot import Config

from pyrogram import Client, filters

from pyrogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)


@Client.on_inline_query(filters.regex(r"^face") & filters.user(Config.AUTH_USERS))
async def faces_inline(
    c: Client,
    q: InlineQuery,
):
    faces_list: List[str] = [
        "¯\\_(ツ)_/¯",
        "( ͡° ͜ʖ ͡°)",
        "( ͡~ ͜ʖ ͡°)",
        "( ͡◐ ͜ʖ ͡◑))",
        "( ͡◔ ͜ʖ ͡◔)",
        "( ͡⚆ ͜ʖ ͡⚆)",
        "( ͡ʘ ͜ʖ ͡ʘ)",
        "(Jnl)",
        "ヽ༼ຈل͜ຈ༽ﾉ",
        "༼ʘ̚ل͜ʘ̚༽",
        "(╯°□°）╯",
        "(ﾉ◕ヮ◕)ﾉ",
        "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧",
        "(◕‿◕)",
        "(｡◕‿‿◕｡)",
        "(っ◕‿◕)っ",
        "(づ｡◕‿‿◕｡)づ",
        "༼ つ ◕_◕ ༽つ",
        "(ง ͠° ͟ل͜ ͡°)ง",
        "(ง'̀-'́)ง",
        "ᕙ(⇀‸↼‶)ᕗ",
        "(҂⌣̀_⌣́)",
        "ᕦ(ò_óˇ)ᕤ",
        "╚(ಠ_ಠ)=┐",
        "ლ(ಠ益ಠლ)",
        "\\_(ʘ_ʘ)_/",
        "( ⚆ _ ⚆ )",
        "(ಥ﹏ಥ)",
        "﴾͡๏̯͡๏﴿",
        "(◔̯◔)",
        "(ಠ_ಠ)",
        "(ಠ‿ಠ)",
        "(¬_¬)",
        "(¬‿¬)",
        "\\ (•◡•) /",
        "(◕‿◕✿)",
        "( ͡°( ͡° ͜ʖ( ͡° ͜ʖ ͡°)ʖ ͡°) ͡°)",
    ]
    results: Dict = []
    for i in faces_list:
        results.append(
            InlineQueryResultArticle(
                title=i, input_message_content=InputTextMessageContent(i)
            )
        )
    await q.answer(results)
