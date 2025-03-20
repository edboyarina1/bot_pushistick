from telebot import types

def create_buttons():
    start_button = types.KeyboardButton('старт')
    students_button = types.KeyboardButton('мои студенты')
    stop_button = types.KeyboardButton('стоп')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(start_button, students_button, stop_button)

    return markup