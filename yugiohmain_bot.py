import json
import logging
import os
import urllib.request
from telegram import Update
from telegram.ext import (
    Updater,
    MessageHandler,
    CommandHandler,
    Filters,
    CallbackContext
)

import message_filters

# todo marketplace message limiter
# todo card database lookup
# todo add more discord functionalities
# todo whitelist and admin stuff
# todo cardmarket lookup
# todo marketplace automatic note filter
# todo marketplace automatic card lookup

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Reads all tokens and IDs
bot_token = message_filters.bot_token
main_id = message_filters.main_id
market_id = message_filters.market_id
feedback_id = message_filters.feedback_id

# Initializes filters
main_filter = message_filters.MainFilter()
market_filter = message_filters.MarketFilter()
feedback_filter = message_filters.FeedbackFilter()

# Heroku stuff
heroku_name = "yugiohmain-bot"
heroku_port = int(os.environ.get("PORT"))

# Initializes the updater
# Makes it global so it works for the ds bot
updater = Updater(bot_token)

# YGODB
card_names_db = "https://db.ygorganization.com/data/idx/card/name/en"
card_data_db = "https://db.ygorganization.com/data/card/"


def main():
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(market_filter & Filters.text & feedback_filter & ~Filters.command,
                                          feedback_handler))
    # dispatcher.add_handler(MessageHandler(market_filter & Filters.text & ~Filters.command,  W.I.P.
    #                                      market_handler))
    dispatcher.add_handler(CommandHandler("carta", card_lookup))

    updater.start_webhook(listen="0.0.0.0",
                          port=heroku_port,
                          url_path=bot_token,
                          webhook_url=f"https://{heroku_name}.herokuapp.com/{bot_token}")
    updater.bot.setWebhook(webhook_url=f"https://{heroku_name}.herokuapp.com/{bot_token}")
    # updater.start_polling(drop_pending_updates=True)
    updater.idle()


def feedback_handler(update: Update, context: CallbackContext):
    update.message.forward(feedback_id)


def market_handler(update: Update, context: CallbackContext):
    if "#cerco" not in update.message.text and "#vendo" not in update.message.text:
        update.message.reply_text(
            f"Ciao {update.effective_user.first_name}, non hai inserito un #vendo o #cerco nel tuo "
            f"messaggio, ti consiglio di farlo per aumentare la visilibit?? del tuo post!",
        )


def card_lookup(update: Update, context: CallbackContext):
    message = update.message.text[7:]
    try:
        with urllib.request.urlopen(card_names_db) as url:
            card_json = json.loads(url.read().decode())
            card_id = card_json[message]
            url_card_id = card_data_db + str(card_id[0])
            with urllib.request.urlopen(url_card_id) as url_id:
                card_data_json = json.loads(url_id.read().decode())
                card_effect = card_data_json["cardData"]["en"]["effectText"]
                updater.bot.send_message(main_id, card_effect)
    except:
        updater.bot.send_message(main_id, "Non ho trovato la carta desiderata.")


if __name__ == "__main__":
    main()
