import requests
import bs4
import time
import random
import json
import csv


all_jobs = []

page = 1
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
   # if job.find("a", attrs={"data-testid": "job-item-title"}):
    #    print(job.prettify())
     #   break
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
            all_jobs.append({
                "title": title,
                "company": company,
                "location": location
            })
            
    times = random.uniform(2.5, 6.0)
    time.sleep(times)

with open("jobs.json", "w", encoding="utf-8") as f:
    json.dump(all_jobs, f, ensure_ascii=False, indent=4)

fieldnames = ["title", "company", "location"]
with open("jobs.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_jobs)
print("Fertig, jobs.json und jobs.csv wurden erfolgreich gespeichert")