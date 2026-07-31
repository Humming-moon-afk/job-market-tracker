import requests
import bs4
import time
import random
import json
import csv
import os
import psycopg2

DB_CONFIG = {
    "dbname": "fhir_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}

def init_db():
    with psycopg2.connect(**DB_CONFIG) as conn:  
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255),
                    company VARCHAR(255),
                    location VARCHAR(255),
                    CONSTRAINT unique_job UNIQUE(title, company, location)
                );
            """)
            print("DB 'jobs' ist bereit.")
files_to_remove = ["jobs.csv", "jobs.json"]
def deletePath():
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"Alte Dateien wurden gelöscht: {file}")
page = 1
def scraper():
    jobs = list()
    for i in range(page, 10):
        try:

            website = f"https://www.stepstone.de/jobs/werkstudent/in-68259-mannheim?whereType=autosuggest&radius=50&page={i}&searchOrigin=Resultlist_top-search"
            headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
            }
            data = requests.get(website, headers=headers, timeout=10)
            print(data.status_code)
        except Exception as e:
            print(f"Fehler: {e}")
            continue
        soup = bs4.BeautifulSoup(data.text, "html.parser")
        jobs_articles = soup.find_all("article")
        for job in jobs_articles:
            # Elements über data-at-Attribute suchen
                title_element = job.find("a", attrs={"data-at": "job-item-title"})
                company_element = job.find("span", attrs={"data-at": "job-item-company-name"})
                location_element = job.find("span", attrs={"data-at": "job-item-location"})
        
            # Text extrahieren
                title = title_element.text.strip() if title_element else "Kein Titel"
                company = company_element.text.strip() if company_element else "Keine Firma"
                location = location_element.text.strip() if location_element else "Kein Ort"
        
            # Nur echte Jobs ausgeben
                if title != "Kein Titel":
                    print(f"Job: {title} | Firma: {company} | Ort: {location}")
                    jobs.append({"title": title, "company": company, "location": location})
                    
        times = random.uniform(2.5, 6.0)
        time.sleep(times)
    return jobs

def write_json(data):
    with open("jobs.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

fieldnames = ["title", "company", "location"]
def write_csv(data):
    with open("jobs.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

keywords = [
    # 1. Programmiersprachen (Mehrdeutige Begriffe wie "r" oder "go" präzisiert)
    "python", "java", "javascript", "typescript", "c++", "c#", "php", "sql", "golang", "rust", 
    "kotlin", "swift", "scala", "bash", "powershell", "ruby", "dart", "matlab", "html", "css",
    
    # 2. Frameworks & Data
    "spring", "spring boot", "react", "angular", "vue", "svelte", "next.js", "django", "flask", 
    "fastapi", "express", "dotnet", ".net", "laravel", "symfony", "pandas", "numpy", "pytorch", 
    "tensorflow", "scikit-learn", "ollama", "llama", "langchain", "pgvector", "embeddings", "rag",
    
    # 3. Tools & Infrastructure
    "postgresql", "postgres", "mysql", "mongodb", "redis", "sqlite", "oracle", "elasticsearch", 
    "mariadb", "aws", "azure", "gcp", "docker", "kubernetes", "git", "github", "gitlab", 
    "terraform", "ansible", "jenkins", "linux", "unix", "ci/cd", "rest", "graphql", "api",
    
    # 4. IT-Rollen (Mehrdeutiges "it " durch konkrete IT-Begriffe ersetzt)
    "informatik", "medieninformatik", "medizininformatik", "software", "developer", "entwickler", 
    "frontend", "backend", "fullstack", "devops", "sysadmin", "administrator", "data science", 
    "data engineer", "data analyst", "ki", "ai", "llm", "machine learning", "deep learning", 
    "security", "cyber", "it-support", "it-consulting", "it-administrator", "cloud", "web", 
    "testing", "qa", "agile", "scrum", "kanban", "automation", "systemplaner", "netzwerk",
    
    # 5. MedTech & Standards
    "fhir", "hl7", "hapi", "ekg", "bio-signal", "time-series", "zeitreihen", "e-health", 
    "digital health", "medizintechnik", "biomedical",
    
    # 6. Arbeitgeber / Big Player
    "roche", "sap", "siemens", "healthineers", "abb", "mvv", "fuchs", "bilfinger", "hays", 
    "ey", "pwc", "kpmg", "deloitte", "mercedes", "daimler", "zeiss", "edeka", "lufthansa", 
    "deutsche bahn", "bosch", "freudenberg", "chg-meridian", "goldbeck", "io-consultants", 
    "comselect", "d-fine", "contact software", "locate-risk", "acteno", "alpine eagle"
]
def filterFunction(scrapedData, keywords):
    filteredResults = []
    for data in scrapedData:
            search_text = f"{data['title']} {data['company']} {data['location']}".lower()
            for keyword in keywords:
                if((keyword) in search_text):
                    filteredResults.append(data)
                    break
    return filteredResults
def save_to_postgres(data):
    if not data:
        print("nichts zum speichern vorhanden")
        return
    job_tuples = [(job["title"], job["company"], job["location"]) for job in data]
    insert_query = """
        INSERT INTO jobs(title, company, location)
        VALUES(%s,%s,%s)
        ON CONFLICT(title, company, location) DO NOTHING;
    """


    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.executemany(insert_query, job_tuples)
            print(f"PostgreSQL: {cur.rowcount} neue Jobs")

init_db()
deletePath()
scrapedData = scraper()
filterScrap = filterFunction(scrapedData, keywords)
save_to_postgres(filterScrap)
write_csv(filterScrap)
write_json(filterScrap)
print("Fertig, jobs.json und jobs.csv und DB wurden erfolgreich gespeichert")