import requests
import bs4
#defined website
website = "https://www.stepstone.de/jobs/werkstudent/in-68259?radius=40"
#header to identify
headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
}
data = requests.get(website, headers=headers)
print(data.status_code)
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