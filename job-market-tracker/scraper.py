import os
import psycopg2
from bs4 import BeautifulSoup
from curl_cffi import requests

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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.google.com",
        "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    
    try:
        response = requests.get(url, timeout=15, impersonate="chrome")
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Fehler: {e}")
        return None




html = fetch_page("https://www.stepstone.de/jobs/werkstudent-in/in-deutschland?radius=30&searchOrigin=Resultlist_top-search&whatType=autosuggest&q=Werkstudent%2Fin")
# print(html)

