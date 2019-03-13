import connection

@connection.connection_handler
def delete_answer(cursor, q_id, a_id):
    cursor.execute("""
    delete from comment
    where question_id = %(q_id)s or answer_id  = %(a_id)s; 
    delete from answer
    where question_id = %(q_id)s and id  = %(a_id)s
    """,
                   {'q_id': q_id, 'a_id': a_id})


@connection.connection_handler
def collect_answers(cursor, q_id):
    cursor.execute("""
    SELECT * from answer
    where question_id = %(q_id)s
    """,
                   {'q_id': q_id})
    result = cursor.fetchall()
    return result


@connection.connection_handler
def find_answer(cursor, a_id):
    cursor.execute("""
    SELECT * from answer
    where id = %(a_id)s
    """,
                   {'a_id': a_id})
    result = cursor.fetchall()
    return result


@connection.connection_handler
def update_answer(cursor, datas):
    cursor.execute("""
                    UPDATE answer
                    SET message=%s, image=%s 
                    WHERE id=%s""",
                   (datas['message'], datas['image'], int(datas['id'])))


@connection.connection_handler
def collect_all_answer(cursor):
    cursor.execute("""
        SELECT * FROM answer
        """)
    result = cursor.fetchall()
    return result


@connection.connection_handler
def add_answer(cursor, form_data):
    cursor.execute("""
                INSERT INTO answer(submission_time, vote_number, question_id, message, image,user_id,accepted)
                VALUES (%s, %s, %s, %s, %s,%s,%s)""",
                   (form_data['submission_time'], form_data['vote_number'], form_data['question_id'],
                    form_data['message'], form_data['image'], form_data['user_id'], form_data['accepted']))


@connection.connection_handler
def accept_answer(cursor, a_id):
    cursor.execute("""
    Update answer 
    set accepted = TRUE
    where id = %(a_id)s
    """,
                   {'a_id': a_id})


@connection.connection_handler
def update_vote_number_answer(cursor, vote, a_id):
    cursor.execute("""
        UPDATE answer
        set vote_number = %(vote)s
        WHERE id = %(a_id)s
    """,
        {'vote': vote, 'a_id': a_id})


@connection.connection_handler
def update_view_number(cursor, q_id):
    cursor.execute("""
    update question
    set view_number = view_number+1
    where id = %(q_id)s
    """,
                   {'q_id': q_id})


@connection.connection_handler
def update_reputation(cursor,user_id,new_reputation):
    cursor.execute("""
    UPDATE "user"
    SET reputation = %(new_reputation)s
    WHERE id = %(user_id)s
    """,
                   {'user_id':user_id, 'new_reputation':new_reputation})


@connection.connection_handler
def get_userid_used_answer(cursor,a_id):
    cursor.execute("""
    SELECT user_id FROM answer
    WHERE id = %(a_id)s
    """,
                   {'a_id':a_id})

    result = cursor.fetchall()
    return result


@connection.connection_handler
def get_reputation(cursor,user_id):
    cursor.execute("""
    SELECT reputation FROM "user"
    WHERE id = %(user_id)s
    """,
                   {'user_id':user_id})
    result = cursor.fetchone()
    return result


@connection.connection_handler
def get_all_answes_form_user(cursor, u_id):
    cursor.execute("""Select question_id, question.title as question_title, answer.message as answer, answer.vote_number as vote_number from answer
    join question on question_id=question.id
    where answer.user_id= %(u_id)s
    """,
                   {'u_id':u_id})
    result=cursor.fetchall()
    return result
