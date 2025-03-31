from src.data import fetch_data, get_tomorrow_lessons, get_ungraded_lessons

def send_tomorrow_notifications(bot, config):
    """Отправляет уведомления преподавателям о занятиях на завтра"""
    
    df = fetch_data(config['table_token'], config['sheet_name'])
    lessons = get_tomorrow_lessons(df)

    if not lessons.empty:
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

        bot.send_message(config['chat_id'], combined_message.strip())


def send_ungraded_notifications(bot, config):
    """Напоминалка о непоставленных оценках"""
    df = fetch_data(config['table_token'], config['sheet_name'])
    ungraded_lessons = get_ungraded_lessons(df)

    if not ungraded_lessons.empty:
        messages = {}
        for _, row in ungraded_lessons.iterrows():
            username = row['Телеграмм']
            student = row['Студент']
            lesson_date = row['Дата'].strftime('%d.%м.%Y')
            time = row['Время']
            if username not in messages:
                messages[username] = []
            messages[username].append(f" {lesson_date}, студент {student}, время {time}")

        combined_message = "Напоминание о непоставленных оценках:\n\n"
        for user, lessons_list in messages.items():
            combined_message += f"{user}, вы забыли поставить оценку за:\n" + "\n".join(lessons_list) + "\n\n"

        bot.send_message(config['chat_id'], combined_message.strip())