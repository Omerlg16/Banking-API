from Config.database import get_connection

def create_user(email, password_hash):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (email, password_hash) VALUES (%s, %s)", (email, password_hash))
    connection.commit()
    connection.close()


def find_by_email(email):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    resultat = cursor.fetchone()
    connection.close()
    return resultat