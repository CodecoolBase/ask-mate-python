import csv
from datetime import datetime


def read_file(filename):
    with open(filename, "r", encoding='utf-8') as f:
        reader_file = csv.DictReader(f)
        datas = []
        for line in reader_file:
            datas.append(dict(line))
        return datas


def sort_file():
    questions = read_file('sample_data/question.csv')
    questions.sort(key=lambda line: line['submission_time'], reverse=True)
    return questions


def formatted_file():
    sorted_questions = sort_file()
    datas = []
    for question in sorted_questions:
        ts = int(question['submission_time'])
        question['submission_time'] = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        datas.append(question)
    return datas

"""
def write_to_file(filename, user_story):
    with open(filename, 'a', encoding='utf-8') as csvfile:
        datas_to_export = csv.DictWriter(csvfile)
        datas_to_export.writerow(user_story)
"""