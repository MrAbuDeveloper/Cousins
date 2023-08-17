from telebot import TeleBot
from config import TOKEN
from telebot.types import Message, ReplyKeyboardRemove
from keyboards import get_wikipedia_button
import wikipedia
from telebot.storage import StateMemoryStorage
from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup

state_storage = StateMemoryStorage()

bot = TeleBot(TOKEN, state_storage=state_storage)


class FirstState(StatesGroup):
    wiki = State()



@bot.message_handler(commands=['start'])
def start(message: Message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    bot.send_message(chat_id, f"Salom, {first_name}!",
                     reply_markup=get_wikipedia_button())


# ## @bot.message_handler(regexp='🌎 Wikipedia')
# @bot.message_handler(func=lambda message: message.text == '🌎 Wikipedia')
# def reaction_to_wiki(message: Message):
#     msg = bot.send_message(message.chat.id,
#                      'Siz nima haqida ma\'lumot olishni istaysiz?', reply_markup=ReplyKeyboardRemove())
#
#     bot.register_next_step_handler(msg, wiki_func)
#
# def wiki_func(message: Message):
#     text = message.text
#     chat_id = message.chat.id
#     wikipedia.set_lang('uz')
#
#     try:
#         result = wikipedia.summary(text)
#         bot.send_message(chat_id, result, reply_markup=get_wikipedia_button())
#     except:
#         bot.send_message(chat_id,"Siz kiritgan ma'lumotni topa olmadim 😞",
#                          reply_markup=get_wikipedia_button() )

@bot.message_handler(func=lambda message: message.text == '🌎 Wikipedia')
def reaction_to_wiki(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    bot.set_state(from_user_id, FirstState.wiki, chat_id)
    bot.send_message(chat_id, 'Siz nima haqida ma\'lumot olishni istaysiz?',
                     reply_markup=ReplyKeyboardRemove())

@bot.message_handler(content_types=['text'], state=FirstState.wiki)
def reaction_to_state(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    text = message.text
    wikipedia.set_lang('uz')
    try:
        result = wikipedia.summary(text)
        bot.send_message(chat_id, result, reply_markup=get_wikipedia_button())
    except:
        bot.send_message(chat_id,"Siz kiritgan ma'lumotni topa olmadim 😞",
                         reply_markup=get_wikipedia_button() )
    bot.delete_state(from_user_id, chat_id)


bot.add_custom_filter(custom_filters.StateFilter(bot))

bot.polling()

