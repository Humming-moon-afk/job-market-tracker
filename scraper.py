import os
import psycopg2
from bs4 import BeautifulSoup
from curl_cffi import requests
import time
import random
from random import uniform

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "job_market_db"),
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



def save_to_db(jobs):
    with psycopg2.connect(**DB_CONFIG) as connector:
        with connector.cursor() as cursor:
            job_data = [(j["title"], j["url"], j["company"], j["location"]) for j in jobs]
            cursor.executemany("""INSERT INTO jobs (title, url, company, location) VALUES (%s, %s, %s, %s) ON CONFLICT (url) DO NOTHING;
            """, job_data)




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



def parse_jobs(html_content):
    if not html_content:
        return []
    jobs = []
    soup = BeautifulSoup(html_content, "html.parser")
    articles = soup.find_all("article")
    for article in articles:
        # fetch data
        title_tag = article.find(attrs={"data-at": "job-item-title"})
        company_tag = article.find(attrs={"data-at": "job-item-company-name"})
        location_tag = article.find(attrs={"data-at": "job-item-location"})
        # test
        title = title_tag.text.strip() if title_tag else ""
        url = title_tag.get("href") if title_tag else ""
        if url.startswith("/"):
            url = "https://www.stepstone.de" + url
        company = company_tag.text.strip() if company_tag else ""
        location = location_tag.text.strip() if location_tag else ""
        if title and url:
            jobs.append({"title": title, "url": url, "company": company, "location": location})
    return jobs





create_table()


for page in range(1, 51):

    # Zukünftige Keyword zulegung:
    # city = ["Mannheim", "Ludwigshafen"]
    # per fString z.B. 
    # f"https://www.stepstone.de/jobs/werkstudent-in/
    # hier --> in-deutschland?whatType=autosuggest&
    # radius=30&page={page}&q=Werkstudent%2fin&
    # searchOrigin=Resultlist_top-search"
    # zu   --> in-{city}
    
    url = f"https://www.stepstone.de/jobs/werkstudent-in/in-deutschland?whatType=autosuggest&radius=30&page={page}&q=Werkstudent%2fin&searchOrigin=Resultlist_top-search"
    html = fetch_page(url)
    jobs = parse_jobs(html)
    if len(jobs) == 0:
        print("Keine weiteren jobs verfügbar")
        break
    save_to_db(jobs)
    print(f"Seite {page}: {len(jobs)} Jobs verarbeitet")
    time.sleep(random.uniform(2, 4))