import connection
from datetime import datetime

ANSWER_PATH = 'sample_data/answer.csv'
QUESTION_PATH = 'sample_data/question.csv'


def sort_file(file_name=QUESTION_PATH, dict_key='submission_time'):
    questions = connection.read_file(file_name)
    questions.sort(key=lambda line: line[dict_key], reverse=True)
    return questions


def format_file():
    sorted_questions = sort_file()
    datas = []
    for question in sorted_questions:
        ts = int(question['submission_time'])
        question['submission_time'] = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        datas.append(question)
    return datas


def generate_new_id(filename):
    new_id = len(connection.read_file(filename)) + 1
    return new_id
