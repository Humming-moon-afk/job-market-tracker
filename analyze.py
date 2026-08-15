import psycopg2
import os
import pandas as pd
import matplotlib.pyplot as plt

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "job_market_db"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432")
}


def connect_to_db():
    with psycopg2.connect(**DB_CONFIG) as connector:
        df = pd.read_sql_query("SELECT * FROM jobs;", connector)
    return df

df = connect_to_db()

top_companies = (df["company"].value_counts().head(10))

top_companies.plot(kind="barh", color="royalblue")
plt.title("Top 10 Arbeitsgeber für Werkstudenten")
plt.xlabel("Anzahl der Stellen")
plt.ylabel("Unternehmen")
plt.tight_layout()
plt.savefig("top_companies.png")