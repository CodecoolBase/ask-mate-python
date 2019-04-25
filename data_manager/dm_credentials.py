from connection import connection_handler


@connection_handler
def register_user(cursor, form_data, hashed_password):
    # form_data.username.data, form_data.email.data etc...
    cursor.execute("""
                    INSERT INTO users (username, name, email, password)
                    VALUES (%(username)s, %(name)s, %(email)s, %(password)s)
                    """, {'username': form_data.username.data,
                          'name': form_data.name.data,
                          'email': form_data.email.data,
                          'password': hashed_password})


@connection_handler
def get_user_data(cursor, email):
    cursor.execute("""
                    SELECT * FROM users
                    WHERE email = %(email)s
                    """,
                   {'email': email})
    user_data = cursor.fetchone()
    return user_data