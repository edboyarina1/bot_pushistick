import os
import logging
from dotenv import load_dotenv, find_dotenv
import telebot
from src.google_sheets import fetch_data, get_tomorrow_lessons, get_ungraded_lessons

env_path = find_dotenv("../.env")
load_dotenv(env_path)

# TODO: заменить на конфиг
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

    @bot.message_handler(commands=['check'])
    def send_ungraded_notifications(message):
        """Напоминалка о непоставленных оценках"""
        df = fetch_data(TOKEN_FOR_TABLE, SHEET_NAME)
        ungraded_lessons = get_ungraded_lessons(df)

        if ungraded_lessons.empty:
            bot.send_message(OWNER_CHAT_ID, "Все занятия оценены.")
            return

        messages = {}
        for _, row in ungraded_lessons.iterrows():
            username = row['Телеграмм']
            student = row['Студент']
            lesson_date = row['Дата'].strftime('%d.%m.%Y')
            time = row['Время']
            if username not in messages:
                messages[username] = []
            messages[username].append(f" {lesson_date}, студент {student}, время {time}")

        combined_message = "Напоминание о непоставленных оценках:\n\n"
        for user, lessons_list in messages.items():
            combined_message += f"{user}, вы забыли поставить оценку за:\n" + "\n".join(lessons_list) + "\n\n"

        bot.send_message(OWNER_CHAT_ID, combined_message.strip())

    return bot
