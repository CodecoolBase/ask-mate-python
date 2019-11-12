import connection
import datetime
from datetime import datetime


QUESTION_HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER_HEADERS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]


def get_single_line_by_id(story_id, filename):
    all_stories = connection.read_file(filename)

    for story in all_stories:
        if story["id"] == story_id:
            story["submission_time"] = datetime.fromtimestamp(int(story["submission_time"]))
            return story


def get_all_questions(filename):
    all_questions = connection.read_file(filename)
    modded_questions = []

    for question in all_questions:
        question["submission_time"] = datetime.fromtimestamp(int(question["submission_time"]))
        modded_questions.append(question)

    return modded_questions


def get_csv_file(filename):
    return connection.read_file(filename)


def get_answers_to_question(question_id, answers_file):
    all_answers = connection.read_file(answers_file)
    answers_to_question = []

    for answer in all_answers:
        if answer["question_id"] == question_id:
            answer["submission_time"] = datetime.fromtimestamp(int(answer["submission_time"]))
            answers_to_question.append(answer)

    return answers_to_question


def fill_out_missing_data(new_data):
    """Fills out the missing data in the new question/answer(id, date, view number, vote number)"""
    new_data['submission_time'] = datetime.datetime.now()
    return new_data
