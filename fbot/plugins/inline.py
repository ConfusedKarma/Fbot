from typing import Dict, List
from fbot import Config

from pyrogram import Client, filters

from pyrogram.errors import (
    PeerIdInvalid,
    UserIdInvalid,
    UsernameInvalid,
)
from pyrogram.types import (
    InlineKeyboardMarkup,
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


@Client.on_inline_query(filters.regex(r"^html") & filters.user(Config.AUTH_USERS))
async def html_inline(
    c: Client,
    q: InlineQuery,
):
    queryinputres = q.query.split(None, 1)[1]
    querytxt, querybuttons = button_parser(queryinputres)
    await q.answer(
        [
            InlineQueryResultArticle(
                title=("html send inline"),
                input_message_content=InputTextMessageContent(
                    querytxt, parse_mode="html"
                ),
                reply_markup=(
                    InlineKeyboardMarkup(querybuttons)
                    if len(querybuttons) != 0
                    else None
                ),
            )
        ]
    )


@Client.on_inline_query(filters.regex(r"^info"))
async def info_inline(
    c: Client,
    q: InlineQuery,
):
    try:
        if q.query == "info":
            user = q.from_user
        elif q.query.lower().split(None, 1)[1]:
            txt = q.query.lower().split(None, 1)[1]
            user = await c.get_users(txt)
    except (PeerIdInvalid, UsernameInvalid, UserIdInvalid):
        await q.answer(
            [
                InlineQueryResultArticle(
                    title=("cant found user"),
                    input_message_content=InputTextMessageContent(
                        ("cant found user")
                    ),
                )
            ]
        )
    await q.answer(
        [
            InlineQueryResultArticle(
                title=("user info send"),
                input_message_content=InputTextMessageContent(
                    ("user info").format(
                        usernameformat=user.username,
                        useridformat=user.id,
                        userdcformat=user.dc_id,
                        usermentionformat=user.mention(),
                    ),
                ),
            )
        ]
    )
