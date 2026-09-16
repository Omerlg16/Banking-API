from Config.database import get_connection

def create_user_with_account(email, password_hash, solde_initial=0):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (email, password_hash) VALUES (%s, %s) RETURNING id",
            (email, password_hash)
        )
        user_id = cursor.fetchone()[0]

        cursor.execute(
            "INSERT INTO accounts (user_id, client, solde) VALUES (%s, %s, %s) RETURNING id",
            (user_id, email, solde_initial)
        )
        account_id = cursor.fetchone()[0]

        connection.commit()
        return user_id, account_id
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def find_by_email(email):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, email, password_hash FROM users WHERE email = %s", (email,))
        return cursor.fetchone()
    finally:
        connection.close()