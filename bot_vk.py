# -*- coding: utf-8 -*-
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import VK_TOKEN
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from common_functions import get_random_question, redis_db, check_answer
from questions_answers import questions_and_answers


vk_session = vk_api.VkApi(token=VK_TOKEN)
vk_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


def send_message_with_keyboard(user_id, message, keyboard):
    vk_api.messages.send(
        user_id=user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message=message
    )


keyboard = VkKeyboard(one_time=True)
keyboard.add_button('Новый вопрос', color=VkKeyboardColor.POSITIVE)
keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        user_answer = event.text
        chat_id = event.user_id
        if user_answer == '/start' or user_answer.lower() == 'начать':
            send_message_with_keyboard(chat_id, 'Привет! Я бот-викторина. Нажми "Новый вопрос", чтобы начать.',
                                       keyboard)
        elif user_answer == 'Новый вопрос':
            random_question = get_random_question()
            redis_db.set(chat_id, random_question)
            send_message_with_keyboard(chat_id, f"Вопрос: {random_question}", keyboard)
        else:
            correct_answer = questions_and_answers.get(redis_db.get(chat_id).decode('utf-8'))
            if user_answer.lower() == 'сдаться':
                send_message_with_keyboard(chat_id,
                                           f"Вот тебе правильный ответ: {correct_answer} Попробуйте следующий вопрос.",
                                           keyboard)
            elif check_answer(user_answer, correct_answer):
                send_message_with_keyboard(chat_id, "Правильно! Попробуйте следующий вопрос.", keyboard)
            else:
                send_message_with_keyboard(chat_id,
                                           f"Неправильно. Правильный ответ: {correct_answer} Попробуйте следующий вопрос.",
                                           keyboard)
