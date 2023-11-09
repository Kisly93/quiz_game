import os
import random


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

print(f"Выбран файл: {selected_file_name}")
