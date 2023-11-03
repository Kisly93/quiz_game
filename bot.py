import telebot
import redis
from telebot import types
import random
from questions_answers import questions_and_answers
from config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, TELEGRAM_BOT_API

redis_db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=0)
bot = telebot.TeleBot(TELEGRAM_BOT_API)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я - бот викторины.")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Новый вопрос')
    item2 = types.KeyboardButton('Сдаться')
    item3 = types.KeyboardButton('Мой счет')
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, "Нажмите новый вопрос для начала викторины!\n /cansel - для выхода",
                     reply_markup=markup)


@bot.message_handler(commands=['cansel'])
def command_default(message):
    bot.send_message(message.chat.id, "Команда завершения работы викторины")


@bot.message_handler(func=lambda message: message.text == 'Новый вопрос')
def handle_new_question(message):
    chat_id = message.chat.id
    random_question = random.choice(list(questions_and_answers.keys()))
    redis_db.set(chat_id, random_question)
    bot.send_message(chat_id, f"Вопрос: {random_question}")


@bot.message_handler(func=lambda message: True)
def handle_user_answer(message):
    chat_id = message.chat.id
    user_answer = message.text.lower()
    correct_answer = questions_and_answers.get(redis_db.get(chat_id).decode('utf-8')).lower()

    if user_answer == 'Сдаться':
        bot.send_message(chat_id, f"Вот тебе правильный ответ: {correct_answer} Попробуйте следующий вопрос.")
    elif user_answer == correct_answer.split('.')[0]:
        bot.send_message(chat_id, "Правильно! Попробуйте следующий вопрос.")
    else:
        bot.send_message(chat_id, f"Неправильно. Правильный ответ: {correct_answer} Попробуйте следующий вопрос.")


@bot.message_handler(func=lambda message: message.text == 'Мой счет')
def handle_my_account(message):
    pass


bot.polling(none_stop=True)
