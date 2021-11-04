import json

from telegram import Message
from telegram.ext import MessageFilter

# Reading all tokens and IDs
bot_token = json.load(open("token.json",), )["bot_token"]
main_id = json.load(open("token.json",), )["main_id"]
market_id = json.load(open("token.json",), )["market_id"]
feedback_id = json.load(open("token.json",), )["feedback_id"]


class MarketFilter(MessageFilter):
    def filter(self, message: Message):
        return bool(message.chat.id == market_id)


class MainFilter(MessageFilter):
    def filter(self, message: Message):
        return bool(message.chat.id == main_id)


class FeedbackFilter(MessageFilter):
    def filter(self, message: Message):
        return "#feedback" in message.text


class PostFilter(MessageFilter):
    def filter(self, message: Message):
        return "#cerco" in message.text or "#vendo" in message.text


class BuyFilter(MessageFilter):
    def filter(self, message: Message):
        return "#cerco" in message.text


class SellFilter(MessageFilter):
    def filter(self, message: Message):
        return "#vendo" in message.text
