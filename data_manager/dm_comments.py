from connection import connection_handler
import datetime


@connection_handler
def add_comment_to_question(cursor, form_data, question_id, users_id):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
                    INSERT INTO comment
                    (edited_count, message, question_id, submission_time, users_id)
                    VALUES (0, %(message)s, %(question_id)s, %(time)s, %(users_id)s)
                    """,
                   {'message': form_data['message'], 'question_id': question_id, 'time': time,
                    'users_id': users_id})


@connection_handler
def add_comment_to_answer(cursor, form_data, answer_id, question_id, users_id):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
                    INSERT INTO comment
                    (edited_count, message, answer_id, submission_time, question_id, users_id)
                    VALUES (0, %(message)s, %(answer_id)s, %(time)s, %(question_id)s, %(users_id)s)
                    """,
                   {'message': form_data['message'], 'answer_id': answer_id,
                    'time': time, 'question_id': question_id, 'users_id': users_id})


@connection_handler
def show_question_comments_by_id(cursor, question_id):
    cursor.execute("""
                    SELECT c.*, u.username FROM comment as c
                    LEFT JOIN users as u ON c.users_id = u.id
                    WHERE   question_id = %(question_id)s AND answer_id IS NULL
                    """,
                   {'question_id': question_id})
    comments = cursor.fetchall()
    return comments


@connection_handler
def show_answer_comments_by_id(cursor, question_id):
    cursor.execute("""
                    SELECT c.*, u.username FROM comment as c
                    LEFT JOIN users as u ON c.users_id = u.id
                    WHERE question_id = %(question_id)s;  
                    """,
                   {'question_id': question_id})
    comments = cursor.fetchall()
    return comments


@connection_handler
def get_comment_by_id(cursor, comment_id):
    cursor.execute("""
                    SELECT c.*, u.username FROM comment as c
                    LEFT JOIN users as u ON c.users_id = u.id                    
                    WHERE c.id = %(comment_id)s;
                    """,
                   {'comment_id': comment_id})
    comment = cursor.fetchone()
    return comment


@connection_handler
def update_comment_by_id(cursor, form_data, comment_id):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
                    UPDATE comment
                    SET message = %(message)s, edited_count = edited_count + 1, submission_time = %(time)s
                    WHERE id = %(comment_id)s; 
                    SELECT question_id FROM comment
                    WHERE id = %(comment_id)s;
                    """,
                   {'message': form_data['message'], 'time': time, 'comment_id': comment_id})
    question_id = cursor.fetchone()
    return question_id


@connection_handler
def delete_comment_by_id(cursor, comment_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE id = %(comment_id)s;
                    """,
                   {'comment_id': comment_id})
