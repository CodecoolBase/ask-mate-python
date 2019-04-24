from connection import connection_handler
import datetime
from data_manager import dm_general


@connection_handler
def get_all_sql_answers_by_question_id(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM answer WHERE question_id=%(question_id)s
                    """,
                    {"question_id": question_id})
    answers = cursor.fetchall()
    return answers


@connection_handler
def qet_answer_by_id(cursor, answer_id):
    cursor.execute("""
                    SELECT * FROM answer WHERE id=%(answer_id)s
                    """,
                    {"answer_id": answer_id})
    answer = cursor.fetchone()
    return answer


@connection_handler
def add_sql_answer(cursor, form_data, question_id):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
                    INSERT INTO answer (submission_time, vote_number, question_id, message)
                    VALUES (%(time)s, 0, %(question_id)s, %(answer)s)
                    """, {'time': time, 'question_id': question_id, 'answer': form_data['answer']})


@connection_handler
def delete_answer(cursor, answer_id):
    # delete answer image if exists
    dm_general.remove_image('answer', answer_id)

    # delete answer and all related comments
    cursor.execute(
                """
            DELETE FROM comment WHERE answer_id=%(answer_id)s;
            DELETE FROM answer WHERE id=%(answer_id)s;
                """, {'answer_id': answer_id}
            )


@connection_handler
def update_answer(cursor, answer_id, form_data):
    cursor.execute(
        """
            UPDATE answer SET message=%(answer)s WHERE id=%(answer_id)s
        """, {"answer": form_data['answer'], "answer_id": answer_id}
    )


@connection_handler
def change_answer_vote(cursor, answer_id, value_to_change_vote):
    cursor.execute("""
                    UPDATE answer
                    SET vote_number = vote_number + %(value_to_change_vote)s
                    WHERE id = %(answer_id)s
                    """, {'value_to_change_vote': value_to_change_vote, 'answer_id': answer_id})
    cursor.execute("""
                    SELECT vote_number FROM answer WHERE id=%(answer_id)s
                    """, {'answer_id': answer_id})
    new_vote_number = cursor.fetchone()
    return new_vote_number
