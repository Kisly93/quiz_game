import os
import random

def load_questions_answers():
    questions_directory = os.path.join(os.getcwd(), 'questions')
    files_list = os.listdir(questions_directory)
    selected_file_name = random.choice(files_list)
    selected_file_path = os.path.join(questions_directory, selected_file_name)

    with open(selected_file_path, "r", encoding="KOI8-R") as my_file:
        file_contents = my_file.read().split('\n\n')

    questions_and_answers = {}

    for block in file_contents:
        lines = block.split('\n')
        if lines[0].startswith('Вопрос'):
            question = '\n'.join(lines[1:]).strip()
        elif lines[0].startswith('Ответ'):
            answer = '\n'.join(lines[1:]).strip()
            questions_and_answers[question] = answer
    return questions_and_answers

def get_random_question():
    return random.choice(list(load_questions_answers().keys()))


def check_answer(user_answer, correct_answer):
    return user_answer.lower() == correct_answer.lower().split('.')[0]
