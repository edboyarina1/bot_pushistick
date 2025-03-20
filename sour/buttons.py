from telebot import types

def create_buttons():
    start_button = types.KeyboardButton('старт')
    students_button = types.KeyboardButton('мои студенты')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(start_button, students_button)

    return markup