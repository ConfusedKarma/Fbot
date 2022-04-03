from pyrogram import Client, filters
from os import listdir, remove
from time import sleep, time
from Fbot import fbot


@Client.on_message(Filters.me & Filters.command(['dl'], ['.', '!']))
def download(fbot, message):
    sleep(0.1)
    if message.reply_to_message:
        start = time()
        if message.reply_to_message.document:
            if len(message.text.split()) == 1:
                file_name = message.reply_to_message.document.file_name
                if file_name in listdir("./Downloads/"):
                    message.reply('There is already a file with this name')
                    return
                fbot.download_media(message.reply_to_message, "./Downloads/{}".format(file_name))
                end = time()
                elapsed_time = str(end - start)
                message.edit('File is downloaded\nElapsed time : {}'.format(elapsed_time))
                return
            else:
                file_name = " ".join(message.text.split()[1:]) + ".txt"
                if file_name in listdir("./Downloads/"):
                    message.edit('There is already a file with this name')
                    return
                app.download_media(message.reply_to_message, file_name="./Downloads/{}".format(file_name))
                end = time()
                elapsed_time = str(end - start)
                message.reply('File is downloaded\nFile name : {}\nElapsed time : {}'.format(file_name,
                                                                                            elapsed_time))
                return
        if message.reply_to_message.video:
            if len(message.text.split()) == 1:
                num = 0
                file_name = "video{}.mp4"
                while 1:
                    if file_name.format(num) in listdir("./Downloads/"):
                        num += 1
                    else:
                        break
                app.download_media(message.reply_to_message, file_name="./Downloads/{}".format(file_name.format(num)))
                end = time()
                elapsed_time = str(end - start)
                message.reply('Video is downloaded\nFile name : {}\nElapsed time : {}'.format(file_name,
                                                                                             elapsed_time))
                return
            else:
                file_name = " ".join(message.text.split()[1:]) + ".mp4"
                if file_name in listdir("./Downloads/"):
                    message.edit('There is already a video with this name')
                    return
                fbot.download_media(message.reply_to_message, file_name="./Downloads/{}".format(file_name))
                end = time()
                elapsed_time = str(end - start)
                message.reply('Video is downloaded\nFile name : {}\nElapsed time : {}'.format(file_name,
                                                                                             elapsed_time))
                return
        if message.reply_to_message.audio:
            if len(message.text.split()) == 1:
                num = 0
                file_name = message.reply_to_message.audio.file_name
                while 1:
                    if file_name.format(num) in listdir("./Downloads/"):
                        num += 1
                    else:
                        break
                fbot.download_media(message.reply_to_message, file_name="./Downloads/{}".format(file_name.format(num)))
                end = time()
                elapsed_time = str(end - start)
                message.reply('Music is downloaded\nFile name : {}\nElapsed time : {}'.format(file_name,
                                                                                             elapsed_time))
                return
            else:
                file_name = " ".join(message.text.split()[1:]) + ".mp3"
                if file_name in listdir("./Downloads/"):
                    message.reply('There is already a music with this name')
                    return
                fbot.download_media(message.reply_to_message, file_name="./Downloads/{}".format(file_name))
                end = time()
                elapsed_time = str(end - start)
                message.reply('Music is downloaded\nFile name : {}\nElapsed time : {}'.format(file_name,
                                                                                             elapsed_time))
                return
    else:
        message.reply('You must reply to message')


@Client.on_message(Filters.me & Filters.command(['upl'], ['.', '!']))
def upload(fbot, message):
    file_name = " ".join(message.text.split()[1:])
    if file_name in listdir("./Downloads/"):
        message.delete()
        start = time()
        fbot.send_document(message.chat.id, "./Downloads/{}".format(file_name))
        elapsed = str(time() - start)
        fbot.send_message(message.chat.id, f"Elapsed time : {elapsed}")


@Client.on_message(Filters.me & Filters.command(['rm'], ['.', '!']))
def remove_file(fbot, message):
    if len(message.text.split()) == 2:
        num = 1
        file = message.text.split()[1]
        if file.isdigit():
            for i in listdir("./Downloads/"):
                if num == int(file):
                    remove("./Downloads/{}".format(i))
                    message.reply('Removed successfully')
                    return
                else:
                    num += 1
            message.reply(f'File # {file} not found')


@Client.on_message(filters.command(['dlist'], ['.', '!']))
def download_list(fbot, message):
    downloads = ""
    num = 1
    for i in listdir("./Downloads/"):
        downloads += f"📂 [{num}] {i}\n"
        num += 1
    message.reply("Download list:\n\n<u>                File names                   </u>.        \n"
                 + downloads, parse_mode='HTML') if num != 1 else message.reply('You don't have a file')
