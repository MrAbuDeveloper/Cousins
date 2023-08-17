from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def get_wikipedia_button():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton('🌎 Wikipedia')
    markup.add(btn)
    return markup

