from pyrogram.types import Message, User
from pyrogram import Client
import shlex

from fbot import CUSTOM_CMD, AUTH_USERS
from fbot.sample_config import Config

def get_arg(message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])


def get_args(message):
    try:
        message = message.text
    except AttributeError:
        pass
    if not message:
        return False
    message = message.split(maxsplit=1)
    if len(message) <= 1:
        return []
    message = message[1]
    try:
        split = shlex.split(message)
    except ValueError:
        return message  # Cannot split, let's assume that it's just one long message
    return list(filter(lambda x: len(x) > 0, split))




import heroku3
import asyncio
import sys
from os import environ, execle, path, remove


from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from pyrogram import filters


HEROKU_API = "d9100d76-456b-46aa-b2fe-74b21793f6c6"
HEROKU_APP_NAME = "singhpmbot"
UPSTREAM_REPO_URL = "https://github.com/ConfusedKarma/Fbot"
requirements_path = path.join(
    path.dirname(path.dirname(path.dirname(__file__))), "requirements.txt"
)


async def gen_chlog(repo, diff):
    ch_log = ""
    d_form = "On %d/%m/%y at %H:%M:%S"
    for c in repo.iter_commits(diff):
        ch_log += f"**#{c.count()}** : {c.committed_datetime.strftime(d_form)} : [{c.summary}]({UPSTREAM_REPO_URL.rstrip('/')}/commit/{c}) by `{c.author}`\n"
    return ch_log


async def updateme_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


@Client.on_message(filters.command("update", CUSTOM_CMD) & filters.user(Config.AUTH_USERS))
async def upstream(client, message):
    status = await message.reply("`Checking for updates, please wait....`")
    conf = get_arg(message)
    off_repo = UPSTREAM_REPO_URL
    try:
        txt = "`Oops.. Updater cannot continue due to "
        txt += "some problems occured`\n\n**LOGTRACE:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await status.edit(f"{txt}\n`directory {error} is not found`")
        repo.__del__()
        return
    except GitCommandError as error:
        await status.edit(f"{txt}\n`Early failure! {error}`")
        repo.__del__()
        return
    except InvalidGitRepositoryError as error:
        if conf != "now":
            pass
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    ac_br = repo.active_branch.name
    if ac_br != "master":
        await status.edit(
            f"**[UPDATER]:**` You are on ({ac_br})\n Please change to master branch.`"
        )
        repo.__del__()
        return
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    if "now" not in conf:
        if changelog:
            changelog_str = f"**New UPDATE available for [[{ac_br}]]({UPSTREAM_REPO_URL}/tree/{ac_br}):\n\nCHANGELOG**\n\n{changelog}"
            if len(changelog_str) > 4096:
                await status.edit("`Changelog is too big, view the file to see it.`")
                file = open("output.txt", "w+")
                file.write(changelog_str)
                file.close()
                await app.send_document(
                    message.chat.id,
                    "output.txt",
                    caption=f"Do `!update now` to update.",
                    reply_to_message_id=status.message_id,
                )
                remove("output.txt")
            else:
                return await status.edit(
                    f"{changelog_str}\n\nDo `.update now` to update.",
                    disable_web_page_preview=True,
                )
        else:
            await status.edit(
                f"\n`SinghPmBot is`  **up-to-date**  `with`  **[[{ac_br}]]({UPSTREAM_REPO_URL}/tree/{ac_br})**\n",
                disable_web_page_preview=True,
            )
            repo.__del__()
            return
    if HEROKU_API is not None:
        import heroku3

        heroku = heroku3.from_key(HEROKU_API)
        heroku_app = None
        heroku_applications = heroku.apps()
        if not HEROKU_APP_NAME:
            await status.edit(
                "`Please set up the HEROKU_APP_NAME variable to be able to update userbot.`"
            )
            repo.__del__()
            return
        for app in heroku_applications:
            if app.name == HEROKU_APP_NAME:
                heroku_app = app
                break
        if heroku_app is None:
            await status.edit(
                f"{txt}\n`Invalid Heroku credentials for updating userbot dyno.`"
            )
            repo.__del__()
            return
        await status.edit(
            "`Userbot dyno build in progress, please wait for it to complete.`"
        )
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", "https://api:" + HEROKU_API + "@"
        )
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            remote.push(refspec=f"HEAD:refs/heads/{ac_br}", force=True)
        except GitCommandError as error:
            pass
        await status.edit("`Successfully Updated!\nRestarting, please wait...`")
    else:
        # Classic Updater, pretty straightforward.
        try:
            ups_rem.pull(ac_br)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        await updateme_requirements()
        await status.edit(
            "`Successfully Updated!\nSinghPmBot is restarting... Wait for a second!`",
        )
        # Spin a new instance of bot
        args = [sys.executable, "./resources/startup/deploy.sh"]
        execle(sys.executable, *args, environ)
        return

@Client.on_message(filters.command("restart", CUSTOM_CMD) & filters.user(Config.AUTH_USERS))
async def restart(client, message):
    try:
        ok = await message.reply("Restarting SinghPmBot, It will take few minutes, Please Wait")
        heroku_conn = heroku3.from_key(HEROKU_API)
        server = heroku_conn.app(HEROKU_APP_NAME)
        server.restart()
    except Exception as e:
        await ok.edit(f"Your `HEROKU_APP_NAME` or `HEROKU_API` is Wrong or Not Filled, Please Make it correct or fill it \n\nError: ```{e}```")
