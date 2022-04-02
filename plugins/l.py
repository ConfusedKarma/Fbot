import os
import json
import logging
import datetime

from pyrogram import Client


@Client.on_message()
def message_handler(client, message):
        print("Got Message!", flush=True)
        logger.info("Got Message!")
        print("Saved message", flush=True)
        logger.info("Saved Message")
