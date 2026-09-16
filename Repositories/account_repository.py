from Config.database import get_connection

def find_by_id(account_id):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM accounts WHERE id = %s", (account_id,))
        return cursor.fetchone()
    finally:
        connection.close()

def update_balance(account_id, new_balance):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE accounts SET solde = %s WHERE id = %s", (new_balance, account_id))
        connection.commit()
    finally:
        connection.close()

if __name__ == "__main__":
    compte = find_by_id(1)
    print(compte)