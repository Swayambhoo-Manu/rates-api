import psycopg2


def get_db_connection():
    connection = psycopg2.connect(
        host="rates-db-container",
        dbname="postgres",
        user="postgres",
        password="ratestask",
        port=5432,
    )
    return connection


# host="localhost",
