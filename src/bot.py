import logging
import telebot
from src.backend import send_tomorrow_notifications, send_ungraded_notifications, send_user_lessons
from src.utils import is_admin
from src.key import get_admin_keyboard, get_user_keyboard

logging.basicConfig(level=logging.INFO)

def create_bot(config):
    bot = telebot.TeleBot(config['bot_token'])

    @bot.message_handler(commands=['start'])
    def start_handler(message):
        username = message.from_user.username
        if is_admin(f"@{username}", config):
            bot.send_message(message.chat.id, "Добро пожаловать, господин администратор!", reply_markup=get_admin_keyboard())
        else:
            bot.send_message(message.chat.id, "Привет", reply_markup=get_user_keyboard())

    @bot.message_handler(commands=['push'])
    def send_tomorrow_notifications_bot(message):
        if is_admin(f"@{message.from_user.username}", config):
            send_tomorrow_notifications(bot, config)
        else:
            bot.send_message(message.chat.id, "У вас нет прав для этой команды.")

    @bot.message_handler(commands=['check'])
    def send_ungraded_notifications_bot(message):
        if is_admin(f"@{message.from_user.username}", config):
            send_ungraded_notifications(bot, config)
        else:
            bot.send_message(message.chat.id, "У вас нет прав для этой команды.")

    @bot.message_handler(commands=['my_lessons'])
    def send_user_lessons_bot(message):
        username = f"@{message.from_user.username}"
        send_user_lessons(bot, config, message.chat.id, username)

    return bot
