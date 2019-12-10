import csv
from datetime import datetime
import time

ANSWER_FILE_PATH = 'sample_data/answer.csv'
QUESTION_FILE_PATH = 'sample_data/question.csv'
DATA_HEADER =['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER =['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_all_questions(time=False):
    all_questions = get_list_of_dictionaries_from_csv(QUESTION_FILE_PATH, DATA_HEADER, time)
    return all_questions


def get_all_answers(time=False):
    all_answers = get_list_of_dictionaries_from_csv(ANSWER_FILE_PATH, ANSWER_HEADER, time)
    return all_answers


def get_list_of_dictionaries_from_csv(path, header, time=False):
    with open(path, encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=header)
        all_data = []
        if not time:
            for data in reader:
                if data['id'] != 'id':
                    all_data.append(data)
        else:
            for data in reader:
                if data['id'] != 'id':
                    real_time = datetime.fromtimestamp(int(data['submission_time']))
                    data['submission_time'] = real_time
                    all_data.append(data)
    return all_data


def get_question_by_id(id):
    all_questions = get_all_questions()
    for question in all_questions:
        if question['id'] == id:
            return question


def next_id_generator(path, header):
    data = get_list_of_dictionaries_from_csv(path, header)
    try:
        next_id = int(data[-1]['id']) + 1
    except ValueError:
        next_id = 0
    return next_id

def add_question(question):
    question['id'] = next_id_generator(QUESTION_FILE_PATH, DATA_HEADER)
    question['submission_time'] = date_time_in_timestamp()
    write_the_file(QUESTION_FILE_PATH, question, DATA_HEADER, append=True)

def add_answer(answer, question_id):
    answer['id'] = next_id_generator(ANSWER_FILE_PATH, DATA_HEADER)
    answer['submission_time'] = date_time_in_timestamp()
    answer['question_id'] = question_id
    write_the_file(ANSWER_FILE_PATH, answer, ANSWER_HEADER, append=True)

def write_the_file(file_name, write_elements, header, append=True):
    existing_data = get_all_answers()
    with open(file_name, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=header)
        writer.writeheader()

        for row in existing_data:
            if not append:
                if row['id'] == write_elements['id']:
                    row = write_elements

            writer.writerow(row)

        if append:
            writer.writerow(write_elements)

def one_question(question_id, time=False):
    all_question = get_all_questions(time)
    for question in all_question:
        if question['id'] == question_id:
            return question

def all_answer_for_one_question(question_id):
    answers = []
    all_answer = get_all_answers(time=True)
    for answer in all_answer:
        if answer['question_id'] == str(question_id):
            answers.append(answer)
    return answers

def date_time_in_timestamp():
    return int(time.time())

def real_date_time(timestamp):
    return datetime.fromtimestamp(timestamp)

