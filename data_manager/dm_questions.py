from connection import connection_handler
from data_manager import dm_general
import datetime


@connection_handler
def get_all_questions_sql_sorted_by_submission_time(cursor):
    cursor.execute("""
                    SELECT q.*, u.username FROM question as q 
                    LEFT JOIN users as u ON q.users_id = u.id ORDER BY submission_time DESC
                    """)
    questions = cursor.fetchall()
    return questions


@connection_handler
def get_5_questions_sql_sorted_by_submission_time(cursor):
    cursor.execute("""
                    SELECT q.*, u.username FROM question as q 
                    LEFT JOIN users as u ON q.users_id = u.id ORDER BY submission_time DESC LIMIT 5
                    """)
    questions = cursor.fetchall()
    return questions


@connection_handler
def get_questions_sorted(cursor, order_by, order_direction):
    cursor.execute(f"""
                    SELECT question.*, users.username FROM question
                    LEFT JOIN users ON users_id = users.id ORDER BY {order_by} {order_direction}
                    """)
    questions = cursor.fetchall()
    return questions


@connection_handler
def get_question_sql_by_id(cursor, id):
    cursor.execute(f"""
                        SELECT question.*, users.username FROM question
                        LEFT JOIN users ON users_id = users.id
                        WHERE question.id={id}
""")
    list_with_question = cursor.fetchall()
    if list_with_question:
        return list_with_question[0]
    else:
        return None


@connection_handler
def qet_users_id_by_question_id(cursor, question_id):
    cursor.execute("""
                    SELECT users_id FROM question WHERE id=%(question_id)s
                    """,
                    {"question_id": question_id})
    question = cursor.fetchone()
    return question['users_id']


@connection_handler
def add_question_sql(cursor, form_data, user_id):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # todo > in every data manager > queries need to be remade in a safe way > like below, without f strings
    cursor.execute("""
                    INSERT INTO question (users_id, submission_time, view_number, vote_number, title, message)
                    VALUES (%(users_id)s, %(time)s, 0, 0, %(title)s, %(message)s)
                    """, {'time': time, 'title': form_data['title'], 'message': form_data['message'], 'users_id': user_id})


@connection_handler
def update_question_sql(cursor, id, form_data):
    cursor.execute("""
                    UPDATE question
                    SET  title = %(title)s, message = %(message)s 
                    WHERE id = %(id)s
                    """,
                   {'title': form_data['title'], 'message': form_data['message'], 'id': id})


@connection_handler
def update_question_view_increase_count(cursor, id):
    cursor.execute(f"""
                    UPDATE question
                    SET view_number = view_number + 1
                    WHERE id = '{id}'
                    """)


@connection_handler
def delete_question(cursor, id):
    # delete question image if exists
    dm_general.remove_image('question', id)

    # delete question and all related data
    cursor.execute(
                # todo > check why there need to be semicolon in the query
                f"""
            DELETE FROM comment WHERE question_id={id};
            DELETE FROM comment WHERE answer_id IN (SELECT id FROM answer WHERE question_id={id});
            DELETE FROM answer WHERE question_id={id};
            DELETE FROM question_tag WHERE question_id={id};
            DELETE FROM question WHERE id={id};
                """
            )


@connection_handler
def change_question_vote(cursor, question_id, value_to_change_vote):
    cursor.execute(f"""
                    UPDATE question
                    SET vote_number = vote_number + {value_to_change_vote}
                    WHERE id = {question_id}
                    """)
    cursor.execute(f"""
                    SELECT vote_number FROM question WHERE id={question_id}
                    """)
    new_vote_number = cursor.fetchone()
    return new_vote_number
