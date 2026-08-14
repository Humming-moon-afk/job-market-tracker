import os
import psycopg2
import requests

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "fhirdb"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432")
}


def create_table():
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

def fetch_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Fehler: {e}")
        return None
    