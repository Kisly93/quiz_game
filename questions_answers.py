import logging
import os
import random
import argparse




def is_file(filename):
    if os.path.isfile(filename):
        return filename


def load_questions_answers(questions_and_answers=None, questions_file=None):

    if questions_and_answers is not None:
        return questions_and_answers

    if questions_file is not None:
        if not os.path.isfile(questions_file):
            raise FileNotFoundError(f"Файл вопросов не найден: {questions_file}")
        else:
            selected_file_path = questions_file
    else:
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


def get_random_question(questions_file=None):
    return random.choice(list(load_questions_answers(questions_file).keys()))


def check_answer(user_answer, correct_answer):
    return user_answer.lower() == correct_answer.lower().split('.')[0]


def parse_arguments():
    parser = argparse.ArgumentParser(description='Обработка вопросов и ответов.')
    parser.add_argument('--questions_file', type=is_file,
                        help='Путь к файлу с вопросами и ответами')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    questions_file = args.questions_file
    logger = logging.getLogger('qa_logger')
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('qa_log.txt')
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    try:
        questions_and_answers = load_questions_answers(questions_file)
        logger.info(f'Вопросы и ответы загружены из файла: {questions_file}')
    except FileNotFoundError as e:
        logger.error(f"Файл вопросов не найден: {str(e)}")
    except Exception as e:
        logger.error(f"Произошла ошибка при загрузке файлов: {str(e)}")