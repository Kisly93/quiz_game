with open("3f15.txt", "r", encoding="KOI8-R") as my_file:
    file_contents = my_file.read().split('\n\n')

questions_and_answers = {}

for block in file_contents:
    lines = block.split('\n')
    if lines[0].startswith('Вопрос'):
        question = '\n'.join(lines[1:]).strip()
    elif lines[0].startswith('Ответ'):
        answer = '\n'.join(lines[1:]).strip()
        questions_and_answers[question] = answer
