import logging
import telebot
import yaml
from src.backend import send_tomorrow_notifications, send_ungraded_notifications

logging.basicConfig(level=logging.INFO)

def create_bot(config):
    bot = telebot.TeleBot(config['bot_token'])

    @bot.message_handler(commands=['push'])
    def send_tomorrow_notifications_bot(message):
        send_tomorrow_notifications(bot, config)
       
    @bot.message_handler(commands=['check'])
    def send_ungraded_notifications_bit(message):
        send_ungraded_notifications(bot, config)

    return bot