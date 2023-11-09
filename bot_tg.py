import telebot
from telebot import types
from config import TELEGRAM_BOT_API
from common_functions import get_random_question, redis_db, check_answer
from questions_answers import questions_and_answers

bot = telebot.TeleBot(TELEGRAM_BOT_API)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я - бот викторины.")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Новый вопрос')
    item2 = types.KeyboardButton('Сдаться')
    item3 = types.KeyboardButton('Мой счет')
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, "Нажмите новый вопрос для начала викторины!\n /cancel - для выхода",
                     reply_markup=markup)


@bot.message_handler(commands=['cancel'])
def command_default(message):
    bot.send_message(message.chat.id, "Команда завершения работы викторины")


@bot.message_handler(func=lambda message: True)
def handle_telegram_messages(message):
    chat_id = message.chat.id
    user_answer = message.text
    if user_answer == 'Новый вопрос':
        random_question = get_random_question()
        redis_db.set(chat_id, random_question)
        bot.send_message(chat_id, f"Вопрос: {random_question}")
    else:
        correct_answer = questions_and_answers.get(redis_db.get(chat_id).decode('utf-8'))
        if user_answer.lower() == 'сдаться':
            bot.send_message(chat_id, f"Вот тебе правильный ответ: {correct_answer} Попробуйте следующий вопрос.")
        elif check_answer(user_answer, correct_answer):
            bot.send_message(chat_id, "Правильно! Попробуйте следующий вопрос.")
        else:
            bot.send_message(chat_id, f"Неправильно. Правильный ответ: {correct_answer} Попробуйте следующий вопрос.")


bot.polling(none_stop=True)
