from src.data import fetch_data, get_tomorrow_lessons, get_ungraded_lessons, get_future_lessons_for_user

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
            print("{", row['Дата'], "}", type(row['Дата']), sep="")
            date = row['Дата'].strftime(r'%d.%m.%Y')
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
    print(df['Дата'])
    print(ungraded_lessons['Дата'])
    
    if not ungraded_lessons.empty:
        messages = {}
        for _, row in ungraded_lessons.iterrows():
            username = row['Телеграмм']
            student = row['Студент']
            
            print("{", row['Дата'], "}", type(row['Дата']), sep="")
            lesson_date = row['Дата'].strftime(r'%d.%m.%Y')
            print("done")
            time = row['Время']
            if username not in messages:
                messages[username] = []
            messages[username].append(f" {lesson_date}, студент {student}, время {time}")

        combined_message = "Напоминание о непоставленных оценках:\n\n"
        for user, lessons_list in messages.items():
            combined_message += f"{user}, вы забыли поставить оценку за:\n" + "\n".join(lessons_list) + "\n\n"

        bot.send_message(config['chat_id'], combined_message.strip())

def send_user_lessons(bot, config, chat_id, username):
    """Отправляет пользователю его предстоящие занятия"""
    df = fetch_data(config['table_token'], config['sheet_name'])
    user_lessons = get_future_lessons_for_user(df, username)
    
    if user_lessons.empty:
        bot.send_message(chat_id, "У вас нет запланированных занятий.")
        return

    message_lines = []
    for _, row in user_lessons.iterrows():
        date = row['Дата'].strftime(r'%d.%m.%Y')
        student = row['Студент']
        time = row['Время']
        message_lines.append(f"{date}, студент {student}, время {time}")
    
    full_message = "Ваши предстоящие занятия:\n\n" + "\n".join(message_lines)
    bot.send_message(chat_id, full_message)