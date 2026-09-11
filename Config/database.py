from os import name

import psycopg2
def get_connection():
    connection = psycopg2.connect(
        host = "localhost",
        dbname = "Banque",
        user = "postgres",
        password = "000000",
    )
    return connection
if __name__ == "__main__":
    connection = get_connection()
    print('connexion reussie ')
    connection.close()