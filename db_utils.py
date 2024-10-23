import mysql.connector
from config import password


def db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=password,
            database="vnz_admissions"
        )
        if conn.is_connected():
            return conn
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
    return None


def fetch_data(query):
    conn = db_connection()
    if conn is None:
        return [], []

    cursor = conn.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()
    return records, columns


def fetch_tables():
    query = "SHOW TABLES"
    return fetch_data(query)[0]
