import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="transport_db",
        user="user",
        password="password",
        port="5434"
    )
    return conn