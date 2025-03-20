import telebot
from apscheduler.schedulers.background import BackgroundScheduler
from google_sheets import get_notifications_data, get_user_sessions
from buttons import create_buttons
import logging
import os
from dotenv import load_dotenv

load_dotenv()  

API_TOKEN = os.getenv('API_TOKEN')
OWNER_CHAT_ID = os.getenv('OWNER_CHAT_ID')

bot = telebot.TeleBot(API_TOKEN)
scheduler = BackgroundScheduler()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_bot():
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        chat_id = message.chat.id
        username = message.chat.username
        with open("chat_ids.txt", "a") as file:
            file.write(f"{chat_id}, {username}\n")
        markup = create_buttons()
        bot.send_message(chat_id, "Этот бот используется для отправки уведомлений!", reply_markup=markup)
        logger.info("New user started the bot: %s, %s", chat_id, username)

    @bot.message_handler(commands=['notify'])
    def send_notifications(message):
        notifications = get_notifications_data()
        for notification in notifications:
            schedule_notification(notification)
        bot.reply_to(message, "Уведомления запланированы.")

    @bot.message_handler(commands=['test_notify'])
    def test_notifications(message):
        notifications = get_notifications_data()
        for notification in notifications:
            logger.info("Sending test message to OWNER_CHAT_ID: %s", OWNER_CHAT_ID)
            bot.send_message(OWNER_CHAT_ID, "hi")
        bot.reply_to(message, "Тестовые уведомления отправлены.")

    @bot.message_handler(commands=['my_students'])
    def my_students(message):
        username = message.chat.username
        sessions = get_user_sessions(username)
        if sessions:
            response = "Ваши запланированные занятия:\n"
            for session in sessions:
                response += f"Студент: {session['student']}, Дата: {session['date']}, Время: {session['time']}\n"
        else:
            response = "У вас нет запланированных занятий."
        bot.reply_to(message, response)


    return bot

def schedule_notification(notification):
    """
    Планирует отправку уведомления на заданное время.
    """
    scheduler.add_job(
        send_notification,
        'date',
        run_date=notification['notification_time'],
        args=[notification['telegram_id'], notification['message']]
    )
    logger.info("Notification scheduled for %s at %s", 
                notification['telegram_id'], notification['notification_time'])

def send_notification(telegram_id, message):
    try:
        bot.send_message(telegram_id, message)
        logger.info("Notification sent to %s", telegram_id)
    except Exception as e:
        logger.error("Failed to send notification to %s: %s", telegram_id, e)

scheduler.start()

if __name__ == "__main__":
    bot = create_bot()
    bot.polling()