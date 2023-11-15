# -*- coding: utf-8 -*-
import logging
import os
from dotenv import load_dotenv
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from questions_answers import load_questions_answers, get_random_question, check_answer
from redis_manager import RedisManager


def send_message_with_keyboard(user_id, message, keyboard, vk_api):
    vk_api.messages.send(
        user_id=user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message=message
    )


def main():
    try:
        load_dotenv()
        VK_TOKEN = os.getenv('VK_TOKEN')
        logger = logging.getLogger('tg_logger')
        logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler('vk_log.txt')
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        redis_manager = RedisManager()
        vk_session = vk.VkApi(token=VK_TOKEN)
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button('Новый вопрос', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)
        logger.warning('Бот запущен')

        for event in longpoll.listen():

            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                user_answer = event.text
                chat_id = event.user_id
                if user_answer == '/start' or user_answer.lower() == 'начать':
                    send_message_with_keyboard(chat_id, 'Привет! Я бот-викторина. Нажми "Новый вопрос", чтобы начать.',
                                               keyboard, vk_api)
                elif user_answer == 'Новый вопрос':
                    random_question = get_random_question()
                    redis_manager.get_redis_db().set(chat_id, random_question)
                    send_message_with_keyboard(chat_id, f"Вопрос: {random_question}", keyboard, vk_api)
                else:
                    correct_answer = load_questions_answers().get(
                        redis_manager.get_redis_db().get(chat_id).decode('utf-8'))
                    if user_answer.lower() == 'сдаться':
                        send_message_with_keyboard(chat_id,
                                                   f"Вот тебе правильный ответ: {correct_answer} Попробуйте следующий вопрос.",
                                                   keyboard, vk_api)
                    elif check_answer(user_answer, correct_answer):
                        send_message_with_keyboard(chat_id, "Правильно! Попробуйте следующий вопрос.", keyboard, vk_api)
                    else:
                        send_message_with_keyboard(chat_id,
                                                   f"Неправильно. Правильный ответ: {correct_answer} Попробуйте следующий вопрос.",
                                                   keyboard, vk_api)

    except Exception as e:
        logging.error(f"Произошла ошибка: {str(e)}")


if __name__ == "__main__":
    main()
