import re
from server_python.config import base_url
from flask import request


def check_referer_url(question_id):
    referer_url = request.headers.get("Referer")
    if referer_url != f"{base_url}/question_detail/{question_id}":
        return True
    else:
        return False


def replace_string(matchobj):
    return '<span class="bg-success" style="margin-right:0;">' + matchobj.group(0) + '</span>'


def highlight_search_term(searched_term, sequence):
    new_sequence = re.sub(searched_term, replace_string, sequence, flags=re.I)
    return new_sequence


def truncate_question(question_message, list_type):
    max_length = 250 if list_type == 'home' else 500
    if len(question_message) > max_length:
        return question_message[:max_length] + ' (...)'
    else:
        return question_message


def change_reputation(user_id, value):
    cursor.execute("""
                    UPDATE question
                    SET  title = %(title)s, message = %(message)s 
                    WHERE id = %(id)s
                    """,
                   {'title': form_data['title'], 'message': form_data['message'], 'id': id})