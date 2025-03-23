import time
import logging
import yaml
from datetime import datetime, timedelta
from telebot import TeleBot
from src.google_sheets import fetch_data, get_tomorrow_lessons

logging.basicConfig(level=logging.INFO)

def load_config():
    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
    mode = config['mode']
    return config[mode]

def send_tomorrow_notifications(bot, config):
    """Отправляет уведомления преподавателям о занятиях на завтра"""
    TOKEN_FOR_TABLE = config['TOKEN_FOR_TABLE']
    SHEET_NAME = config['sheet_name']
    OWNER_CHAT_ID = config['OWNER_CHAT_ID']
    
    df = fetch_data(TOKEN_FOR_TABLE, SHEET_NAME)
    lessons = get_tomorrow_lessons(df)

    if lessons.empty:
        bot.send_message(OWNER_CHAT_ID, "На завтра нет запланированных занятий")
    else:
        messages = {}
        for _, row in lessons.iterrows():
            username = row['Телеграмм']
            student = row['Студент']
            time = row['Время']
            date = row['Дата'].strftime('%d.%m.%Y')
            if username not in messages:
                messages[username] = []
            messages[username].append(f"{date}, студент {student}, время {time}")

        combined_message = "Напоминание о занятиях на завтра:\n\n"
        for user, lessons_list in messages.items():
            combined_message += f"{user}, у вас следующие занятия:\n" + "\n".join(lessons_list) + "\n\n"

        bot.send_message(OWNER_CHAT_ID, combined_message.strip())

def main():
    config = load_config()
    BOT_TOKEN = config['API_TOKEN']
    bot = TeleBot(BOT_TOKEN)

if __name__ == "__main__":
    main()