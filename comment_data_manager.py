import connection


@connection.connection_handler
def update_view_number(cursor, q_id):
    cursor.execute("""
    update question
    set view_number = view_number+1
    where id = %(q_id)s
    """,
                   {'q_id': q_id})


@connection.connection_handler
def update_vote_number(cursor, vote, q_id):
    cursor.execute("""
        UPDATE question
        set vote_number = %(vote)s
        WHERE id = %(q_id)s
    """,
                   {'vote': vote, 'q_id': q_id})


@connection.connection_handler
def add_comment_to_question(cursor, q_id, comment_message, u_id, s_time):
    cursor.execute("""
                    insert into comment(question_id, message, user_id, submission_time)
                    values (%(q_id)s,%(comment_message)s,%(u_id)s,%(s_time)s)
                    
    """,
                   {'q_id': q_id, 'comment_message': comment_message, 'u_id': u_id, 's_time': s_time})


@connection.connection_handler
def add_comment_to_answer(cursor, a_id, comment_message):
    cursor.execute("""
                    insert into comment(answer_id, message)
                    values (%(a_id)s,%(comment_message)s)

    """,
                   {'a_id': a_id, 'comment_message': comment_message})


@connection.connection_handler
def collect_comment_to_question(cursor, q_id):
    cursor.execute("""
                    Select message from comment
                    where question_id = %(q_id)s
    """,
                   {'q_id': q_id})
    result = cursor.fetchall()
    return result


@connection.connection_handler
def collect_comment_to_answer(cursor, a_id):
    cursor.execute("""
                    Select message, answer_id from comment
                    where answer_id = %(a_id)s
    """,
                   {'a_id': a_id})
    result = cursor.fetchall()
    return result


@connection.connection_handler
def get_all_comments_from_user(cursor, u_id):
    cursor.execute("""
    Select comment.message as comment, question.title as question, question.id as q_id, answer.question_id as question_id, answer.message as answer from comment
    full join answer on comment.answer_id = answer.id
    full join question on comment.question_id = question.id
    where comment.user_id = %(u_id)s
    """,
                   {'u_id': u_id})
    result = cursor.fetchall()
    return result
