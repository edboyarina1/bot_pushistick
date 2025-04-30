from telebot import types

def get_admin_keyboard():
    """Клавиатура для администратора"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Напоминалка'))
    markup.add(types.KeyboardButton('Проверить оценки'))
    markup.add(types.KeyboardButton('Мои занятия'))
    return markup

def get_user_keyboard():
    """Клавиатура для пользователя """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Мои занятия'))
    return markup

    
   