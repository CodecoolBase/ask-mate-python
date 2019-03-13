import connection


@connection.connection_handler
def insert_new_user(cursor, submission_time, username, h_password, user_reputation):
    cursor.execute("""
    insert into "user" (submission_time, user_name,hashed_password, reputation)
    values (%(submission_time)s, %(username)s, %(h_password)s, %(user_reputation)s)
    """,
    {'submission_time':submission_time,'username': username, 'h_password': h_password, 'user_reputation':user_reputation})


@connection.connection_handler
def find_user(cursor, username):
    cursor.execute("""
    select user_name
    from "user"
    where user_name=%(username)s""",
                   {'username' : username})
    result = cursor.fetchone()
    return result


@connection.connection_handler
def get_user_id(cursor, username):
    cursor.execute("""
    select id from "user"
    where user_name = %(username)s
    """,
                   {'username': username})
    result = cursor.fetchone()
    return result

@connection.connection_handler
def get_hashed_password(cursor, user_name):
    cursor.execute("""
    SELECT hashed_password
    FROM "user"
    WHERE user_name = %(user_name)s
    """,
                   {'user_name' : user_name})
    result = cursor.fetchone()
    return result


@connection.connection_handler
def select_all_user(cursor):
    cursor.execute("""
    select * from "user"
    ORDER BY id
    """)
    result=cursor.fetchall()
    return result


@connection.connection_handler
def get_user_data(cursor, u_id):
    cursor.execute("""
    select id, user_name, submission_time, reputation from "user"
    where id = %(u_id)s
    """,
                   {'u_id': u_id})
    result= cursor.fetchone()
    return result
