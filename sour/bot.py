import os
import logging
from dotenv import load_dotenv, find_dotenv
import telebot
from sour.google_sheets import fetch_data, get_tomorrow_lessons, get_ungraded_lessons

env_path = find_dotenv("../.env")
load_dotenv(env_path)

BOT_TOKEN = os.getenv('API_TOKEN')
TOKEN_FOR_TABLE = os.getenv('TOKEN_FOR_TABLE')
SHEET_NAME = os.getenv('sheet_name')
OWNER_CHAT_ID = os.getenv('OWNER_CHAT_ID')  

logging.basicConfig(level=logging.INFO)

def create_bot():
    bot = telebot.TeleBot(BOT_TOKEN)

    @bot.message_handler(commands=['push'])
    def send_tomorrow_notifications(message):
        """Отправляет уведомления преподавателям о занятиях на завтра"""
        df = fetch_data(TOKEN_FOR_TABLE, SHEET_NAME)
        lessons = get_tomorrow_lessons(df)

        if lessons.empty:
            bot.send_message(OWNER_CHAT_ID, "На завтра нет запланированных занятий")
            return

        for _, row in lessons.iterrows():
            username = row['Телеграмм']
            student = row['Студент']
            time = row['Время']
            text = f"{username}, завтра ({row['Дата'].strftime('%d.%m.%Y')}) у вас занятие со студентом {student} в {time}."
            bot.send_message(OWNER_CHAT_ID, text)


    @bot.message_handler(commands=['check'])
    def send_ungraded_notifications(message):
        """Напоминалка о оценках"""
        df = fetch_data(TOKEN_FOR_TABLE, SHEET_NAME)
        ungraded_lessons = get_ungraded_lessons(df)

        if ungraded_lessons.empty:
            bot.send_message(OWNER_CHAT_ID, "Все занятия оценены.")
            return

        for _, row in ungraded_lessons.iterrows():
            username = row['Телеграмм']
            student = row['Студент']
            lesson_date = row['Дата'].strftime('%d.%m.%Y')
            time = row['Время']
            text = f"{username}, вы не поставили оценку студенту {student} за занятие {lesson_date} в {time}."
            bot.send_message(OWNER_CHAT_ID, text)

    return bot
