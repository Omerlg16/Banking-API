from Config.database import get_connection

def find_by_id(account_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM accounts WHERE id = %s", (account_id,))
    resultat = cursor.fetchone()
    connection.close()
    return resultat
if __name__ == "__main__":
    compte = find_by_id(1)
    print(compte)