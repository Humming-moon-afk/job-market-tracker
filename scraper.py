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
if soup.title:
    print(soup.title.text)
else:
    print("Kein Title-Tag gefunden")

h1_tags = soup.find_all("h1")
for tags in h1_tags:
    print(tags.text)
job_links = soup.find_all("a", attrs={"data-testid" : "job-item-title"})
for jobs in job_links:
    print(jobs.text.strip())