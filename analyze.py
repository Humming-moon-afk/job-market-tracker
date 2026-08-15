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