import os
import redis
from dotenv import load_dotenv
import telebot
import logging
from telebot import types
from questions_answers import load_questions_answers, get_random_question, check_answer

load_dotenv()
bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_API'))
redis_db = redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'),
                             password=os.getenv('REDIS_PASSWORD'), db=0)

user_data = {}


@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id

    questions_and_answers_from_file = load_questions_answers()
    user_data[chat_id] = {'questions_and_answers_from_file': questions_and_answers_from_file}

    bot.send_message(chat_id, "Привет! Я - бот викторины.")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Новый вопрос')
    button2 = types.KeyboardButton('Сдаться')
    button3 = types.KeyboardButton('Мой счет')
    markup.add(button1, button2, button3)
    bot.send_message(chat_id, "Нажмите новый вопрос для начала викторины!\n /cancel - для выхода",
                     reply_markup=markup)


@bot.message_handler(commands=['cancel'])
def command_default(message):
    bot.send_message(message.chat.id, "Команда завершения работы викторины")


@bot.message_handler(func=lambda message: True)
def handle_telegram_messages(message):
    chat_id = message.chat.id
    user_answer = message.text
    questions_and_answers = user_data.get(chat_id, {}).get('questions_and_answers_from_file', {})

    if user_answer == 'Новый вопрос':
        random_question = get_random_question(questions_and_answers)
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


def main():
    logging.basicConfig(filename='tg_log.txt', level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.error(f"Ошибка запуска бота: {str(e)}")


if __name__ == "__main__":
    main()
