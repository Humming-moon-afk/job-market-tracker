import os
import psycopg2

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "fhirdb"),
    "user": os.getenv("DB_USER", "postgre"),
    "password": os.getenv("DB_PASSWORD", "postgre"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432")
}


def create_db():
    with psycopg2.connect(**DB_CONFIG) as connector:
        with connector.cursor() as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS jobs(
            id SERIAL PRIMARY KEY,
            url TEXT UNIQUE,
            title VARCHAR(255),
            location VARCHAR(255),
            company VARCHAR(255)
            );
            """)
create_db()