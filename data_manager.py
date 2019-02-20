import connection
from datetime import datetime


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
def get_comments(cursor):
    cursor.execute("""SELECT * FROM comment ORDER BY submission_time DESC""")
    comments = cursor.fetchall()
    return comments


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


@connection.connection_handler
def search_in_question_table(cursor, searched_word):
    cursor.execute("""SELECT * FROM question WHERE title LIKE %(searched_word)s OR message LIKE %(searched_word)s;""",
                   {searched_word: '%' + searched_word + '%'})
    searched_data = cursor.fetchall()
    return searched_data


@connection.connection_handler
def search_in_answer_table(cursor, searched_word):
    cursor.execute("""SELECT * FROM answer WHERE message LIKE %(searched_word)s;""",
                   {searched_word: '%' + searched_word + '%'})
    searched_data = cursor.fetchall()
    return searched_data


@connection.connection_handler
def vote_up_question(cursor, question_id):

    variables = {
        'question_id': question_id
    }

    cursor.execute("""UPDATE question
                      SET vote_number = vote_number+1
                      WHERE id = %(question_id)s;""", variables)


@connection.connection_handler
def vote_down_question(cursor, question_id):

    variables = {
        'question_id': question_id
    }

    cursor.execute("""UPDATE question
                      SET vote_number = vote_number-1
                      WHERE id = %(question_id)s;""", variables)


@connection.connection_handler
def vote_up_answer(cursor, question_id, answer_id):

    variables = {
        'question_id': question_id,
        'answer_id': answer_id
    }

    cursor.execute("""UPDATE answer
                      SET vote_number = vote_number+1
                      WHERE question_id = %(question_id)s AND id = %(answer_id)s;""", variables)


@connection.connection_handler
def vote_down_answer(cursor, question_id, answer_id):

    variables = {
        'question_id': question_id,
        'answer_id': answer_id
    }

    cursor.execute("""UPDATE answer
                      SET vote_number = vote_number-1
                      WHERE question_id = %(question_id)s AND id = %(answer_id)s;""", variables)
