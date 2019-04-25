from connection import connection_handler
import os
from psycopg2 import sql


@connection_handler
def update_image_path(cursor, table, filename, id):
    cursor.execute(f"""
                    UPDATE {table} 
                    SET image = 'images/{filename}' WHERE id={id}
                    """)


@connection_handler
def remove_image(cursor, table_name, resource_id):
    cursor.execute(
        sql.SQL('select image from {} WHERE id=%s').format(sql.Identifier(table_name)), [resource_id]
    )
    file_path = cursor.fetchone()
    if file_path and file_path['image'] != None:
        os.remove(f"./static/{file_path['image']}")


@connection_handler
def search_results(cursor, search_term):

    cursor.execute("""
            SELECT DISTINCT q.* FROM question q JOIN answer a ON q.id=a.question_id WHERE
            UPPER(q.title) LIKE UPPER(%(search_term)s)
            OR UPPER(q.message) LIKE UPPER(%(search_term)s)
            OR UPPER(a.message) LIKE UPPER(%(search_term)s);
                    """, {'search_term': '%'+search_term+'%'})
    questions = cursor.fetchall()
    cursor.execute("""
            SELECT * FROM answer WHERE UPPER(message) LIKE UPPER(%(search_term)s)
                    """, {'search_term': '%'+search_term+'%'})
    answers = cursor.fetchall()
    return questions, answers
