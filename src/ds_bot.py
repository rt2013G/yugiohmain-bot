from decouple import config

import discord
from telegram.ext import Updater

import message_filters
import yugiohmain_bot

ds_token = config("discord_token")
ds_client = discord.Client()


def send_msg_to_telegram(chat_id, message, updater: Updater):
    updater.bot.send_message(chat_id, message, disable_web_page_preview=True)


@ds_client.event
async def on_ready():
    print(f"{ds_client.user} connected")


@ds_client.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        send_msg_to_telegram(message_filters.main_id, f"{member.display_name} è entrato nel canale {after.channel} su "
                                                      f"discord. \nLink discord: https://discord.gg/cnKQ8eqVe4",
                             yugiohmain_bot.updater)


ds_client.run(ds_token)
