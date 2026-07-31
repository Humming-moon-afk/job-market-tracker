import requests
import bs4
import time
import random
import json
import csv
import os

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

deletePath()
scrapedData = scraper()
keywords = [
    "python", "java", "javascript", "typescript", "c++", "c#", "php", "sql", "html", "css",
    "react", "angular", "vue", "django", "spring", "docker", "kubernetes", "aws", "azure", "git",
    "informatik", "software", "developer", "entwickler", "frontend", "backend", "fullstack",
    "devops", "data science", "data engineer", "ki", "ai", "llm", "sysadmin", "it-", "it ",
    "medieninformatik", "systemplaner", "automation"
]
def filterFunction(scrapedData, keywords):
    filteredResults = []
    for data in scrapedData:
        for keyword in keywords:
            if((keyword) in data["title"].lower()):
                filteredResults.append(data)
                break
    return filteredResults
filterScrap = filterFunction(scrapedData, keywords)
write_csv(filterScrap)
write_json(filterScrap)
print("Fertig, jobs.json und jobs.csv wurden erfolgreich gespeichert")
