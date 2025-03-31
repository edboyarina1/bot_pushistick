import logging

from telebot import TeleBot
from src.utils import load_config
from src.backend import send_tomorrow_notifications

logging.basicConfig(level=logging.INFO)

def main():
    config = load_config()
    bot = TeleBot(config['bot_token'])
    send_tomorrow_notifications(bot, config)

if __name__ == "__main__":
    main()