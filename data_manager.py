import connection
import util
from operator import itemgetter


@connection.connection_handler
def get_answers(cursor, question_id):
    cursor.execute("""SELECT * FROM answer WHERE question_id = (%s)""", (question_id,))
    answers = [dict(row) for row in cursor.fetchall()]
    return answers


@connection.connection_handler
def get_questions(cursor, question_id=None):
    if not question_id:
        cursor.execute("""SELECT * FROM question """)
        questions = [dict(row) for row in cursor.fetchall()]
    else:
        cursor.execute("""SELECT * FROM question WHERE id = (%s)""", (question_id,))
        questions = [dict(row) for row in cursor.fetchall()]
    return questions


@connection.connection_handler
def new_question_manager(cursor, new_question):
    cursor.execute("""INSERT INTO question (title,submission_time, message) VALUES (%s,%s,%s);""", (new_question['title'], util.submission_time(), new_question['message'],))
    cursor.execute("""SELECT id FROM question WHERE title= %(title)s;""", {'title': new_question['title'], 'message': new_question['message']})
    question_id = dict(cursor.fetchone())['id']
    return question_id


@connection.connection_handler
def new_answer_manager(cursor, new_answer):
    cursor.execute("""INSERT INTO answer (submission_time, question_id, message)  VALUES ( %s, %s, %s);""", (util.submission_time(), new_answer['question_id'], new_answer['message'],))


def sorting_questions(sorting_list, reversing):
    sorted(get_questions(), key=itemgetter(sorting_list), reverse=reversing)


@connection.connection_handler
def delete_question(cursor, question_id):
    cursor.execute("""DELETE FROM answer WHERE question_id = (%s)""", (question_id,))
    cursor.execute("""DELETE FROM question WHERE id = (%s)""", (question_id,))
