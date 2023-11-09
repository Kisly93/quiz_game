# -*- coding: utf-8 -*-
import random
import redis
from questions_answers import questions_and_answers
from config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD

redis_db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=0)


def get_random_question():
    return random.choice(list(questions_and_answers.keys()))


def check_answer(user_answer, correct_answer):
    return user_answer.lower() == correct_answer.lower().split('.')[0]
