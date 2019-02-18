import connection
from datetime import datetime
import time


@connection.connection_handler
def get_questions(cursor):
    cursor.execute("""SELECT * FROM question ORDER BY submission_time DESC;""")
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def get_answers(cursor):
    cursor.execute("""SELECT * FROM answer ORDER BY submission_time DESC;""")
    answers = cursor.fetchall()
    return answers


@connection.connection_handler
def add_question(cursor, title, message):
    user_story = {
        'submission_time': datetime.now(),
        'view_number': 0,
        'vote_number': 0,
        'title': title,
        'message': message,
        'image': ""
    }

    cursor.execute("""INSERT INTO question(submission_time, view_number, vote_number, title, message, image)
                      VALUES(%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s);""",
                   user_story)

    cursor.execute("""SELECT id FROM question
                      ORDER BY id DESC
                      LIMIT 1;""")
    return cursor.fetchone()['id']

@connection.connection_handler
def add_answer(cursor, question_id, message):

    user_story = {
        'submission_time': datetime.now(),
        'vote_number': 0,
        'question_id': question_id,
        'message': message,
        'image': ""
    }

    cursor.execute("""INSERT INTO answer(submission_time, vote_number, question_id, message, image)
                      VALUES(%(submission_time)s,%(vote_number)s,%(question_id)s, %(message)s,%(image)s);""", user_story)


def generate_new_id(filename):
    new_id = len(connection.read_file(filename))
    return new_id
