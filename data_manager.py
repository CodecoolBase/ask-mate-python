import connection
from datetime import datetime

ANSWER_PATH = 'sample_data/answer.csv'
QUESTION_PATH = 'sample_data/question.csv'


def sort_file(file_name=QUESTION_PATH, dict_key='submission_time'):
    questions = connection.read_file(file_name)
    questions.sort(key=lambda line: line[dict_key], reverse=True)
    return questions


def format_file(file_path):
    sorted_datas = sort_file(file_name=file_path)
    datas = []
    for data in sorted_datas:
        ts = int(data['submission_time'])
        data['submission_time'] = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        datas.append(data)
    return datas


def get_questions():
    return format_file(QUESTION_PATH)


def get_answers():
    return format_file(ANSWER_PATH)


def generate_new_id(filename):
    new_id = len(connection.read_file(filename))
    return new_id
