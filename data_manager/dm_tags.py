from connection import connection_handler


@connection_handler
def get_tags_of_question_by_id(cursor, question_id):
    cursor.execute("""
                    SELECT DISTINCT * FROM question_tag INNER JOIN tag
                    ON question_tag.tag_id = tag.id
                    WHERE question_tag.question_id = %(question_id)s;
                    """,
                   {'question_id': question_id})
    tags = cursor.fetchall()
    return tags


@connection_handler
def add_tags_to_question(cursor, form_data, question_id):
    # Sample form_data:
    # ImmutableMultiDict([('3', 'on'), ('new_tag', 'ooo')])
    for tag_id, selected in form_data.items():
        # if if iteration is on new_tag and there is no new tag - do nothing
        if not selected:
            continue
        # if iteration is on new_tag and new tak is not empty
        if tag_id == 'new_tag' and selected:
            new_tag = get_tag_data_by_tag_name(selected)
            tag_id = new_tag['id']
        cursor.execute("""
                        INSERT INTO question_tag (question_id, tag_id)
                        VALUES (%(question_id)s, %(tag_id)s)
                        """,
                       {'question_id': question_id, 'tag_id': tag_id})


@connection_handler
def get_tag_data_by_tag_name(cursor, tag_name):
    cursor.execute("""
                    SELECT * FROM tag
                    WHERE name = %(name)s                  
                    """, {'name': tag_name})
    tag = cursor.fetchone()
    return tag


@connection_handler
def get_tags(cursor, question_id):
    cursor.execute("""
                    SELECT tag.id, tag.name FROM tag
                    WHERE tag.id NOT IN (
                        SELECT tag_id FROM question_tag
                        WHERE question_id = %(question_id)s
                        );
                    """,
                   {'question_id': question_id})
    tags = cursor.fetchall()
    return tags


@connection_handler
def add_new_tag(cursor, new_tag):
    # todo > now if we try to add tag which already exists - there is psycopg2.IntegrityError > handle it
    cursor.execute("""
                    INSERT INTO tag (name)
                    VALUES (%(tag_name)s);
                    """,
                   {'tag_name': new_tag})


@connection_handler
def delete_tag_from_question(cursor, question_id, tag_id):
    cursor.execute("""
                    DELETE FROM question_tag
                    WHERE question_id = %(question_id)s AND tag_id = %(tag_id)s;
                    """,
                   {'question_id': question_id, 'tag_id': tag_id})


@connection_handler
def get_tags_and_count(cursor):
    cursor.execute("""
                    SELECT tag.name, count(question_tag.question_id) as used FROM tag 
                    LEFT JOIN question_tag ON tag.id = question_tag.tag_id
                    GROUP BY tag.name;
                    """)
    tags = cursor.fetchall()
    return tags
