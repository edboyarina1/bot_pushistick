from telebot import types

def get_admin_keyboard():
    """Клавиатура для администратора"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('/push'))
    markup.add(types.KeyboardButton('/check'))
    markup.add(types.KeyboardButton('/my_lessons'))
    return markup

def get_user_keyboard():
    """Клавиатура для  пользователя"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('/my_lessons'))
    return markup
