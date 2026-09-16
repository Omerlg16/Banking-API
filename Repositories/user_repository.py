from Config.database import get_connection

def create_user(email, password_hash):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (email, password_hash) VALUES (%s, %s)", (email, password_hash))
        connection.commit()
    finally:
        connection.close()


def find_by_email(email):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        return cursor.fetchone()
    finally:
        connection.close()