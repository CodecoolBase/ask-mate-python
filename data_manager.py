import connection
from datetime import datetime

ANSWER_PATH = 'sample_data/answer.csv'
QUESTION_PATH = 'sample_data/question.csv'


def sort_file(file_name=QUESTION_PATH):
    questions = connection.read_file(file_name)
    questions.sort(key=lambda line: line['submission_time'], reverse=True)
    return questions


def format_file():
    sorted_questions = sort_file()
    datas = []
    for question in sorted_questions:
        ts = int(question['submission_time'])
        question['submission_time'] = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        datas.append(question)
    return datas
