import os
from dotenv import load_dotenv
import telebot
from redis_manager import RedisManager
import logging
from telebot import types
from questions_answers import load_questions_answers, get_random_question, check_answer

load_dotenv()
bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_API'))


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я - бот викторины.")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Новый вопрос')
    button2 = types.KeyboardButton('Сдаться')
    button3 = types.KeyboardButton('Мой счет')
    markup.add(button1, button2, button3)
    bot.send_message(message.chat.id, "Нажмите новый вопрос для начала викторины!\n /cancel - для выхода",
                     reply_markup=markup)


@bot.message_handler(commands=['cancel'])
def command_default(message):
    bot.send_message(message.chat.id, "Команда завершения работы викторины")


@bot.message_handler(func=lambda message: True)
def handle_telegram_messages(message):
    chat_id = message.chat.id
    user_answer = message.text
    redis_manager = RedisManager()
    if user_answer == 'Новый вопрос':
        random_question = get_random_question()
        redis_manager.get_redis_db().set(chat_id, random_question)
        bot.send_message(chat_id, f"Вопрос: {random_question}")
    else:
        correct_answer = load_questions_answers().get(redis_manager.get_redis_db().get(chat_id).decode('utf-8'))
        if user_answer.lower() == 'сдаться':
            bot.send_message(chat_id, f"Вот тебе правильный ответ: {correct_answer} Попробуйте следующий вопрос.")
        elif check_answer(user_answer, correct_answer):
            bot.send_message(chat_id, "Правильно! Попробуйте следующий вопрос.")
        else:
            bot.send_message(chat_id, f"Неправильно. Правильный ответ: {correct_answer} Попробуйте следующий вопрос.")


def main():
    logging.basicConfig(filename='tg_log.txt', level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.error(f"Ошибка запуска бота: {str(e)}")


if __name__ == "__main__":
    main()
