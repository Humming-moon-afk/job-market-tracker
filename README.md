# Job Market Tracker

Ein automatisierter Scraper zur Aggregation und Filterung von IT-Werkstudentenstellen mit automatischer Duplikatvermeidung in PostgreSQL.

## Features

* **Scraping & Parsing:** Extrahiert relevante Stellenausschreibungen via `requests` und `BeautifulSoup`.
* **Regex-Filtering:** Präzise Abfrage von Tech-Keywords über Wortgrenzen (`\b`), um False Positives zu vermeiden.
* **PostgreSQL Storage:** Speichert Jobs relational und verhindert Doppeleinträge über `UNIQUE`-Constraints auf der Job-URL.
* **CI/CD Pipeline:** Automated Linting (`ruff`) und täglicher Cronjob-Workflow via GitHub Actions.

## Tech Stack

* **Sprache:** Python 3.11
* **Database:** PostgreSQL (lokal via Docker)
* **Libraries:** BeautifulSoup4, Requests, Psycopg2
* **CI/CD:** GitHub Actions

## Lokale Einrichtung

### 1. Repository klonen & Virtual Environment erstellen

```bash
git clone [https://github.com/Humming-moon-afk/job-market-tracker.git](https://github.com/Humming-moon-afk/job-market-tracker.git)
cd job-market-tracker

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```bash
docker run --name postgres-jobmarket \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=fhir_db \
  -p 5432:5432 -d postgres

```bash
python scraper.py