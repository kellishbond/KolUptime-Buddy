import sqlite3
from pathlib import Path

DATABASE_FILE = Path(__file__).with_name("uptime.db")


def create_table():
    with sqlite3.connect(DATABASE_FILE) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS check_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                website_url TEXT NOT NULL,
                checked_at TEXT NOT NULL,
                status TEXT NOT NULL,
                response_time REAL,
                http_status_code INTEGER,
                attempts INTEGER NOT NULL
            )
        """)


def save_check(
    website_url,
    checked_at,
    status,
    response_time,
    http_status_code,
    attempts
):
    with sqlite3.connect(DATABASE_FILE) as connection:
        connection.execute("""
            INSERT INTO check_history (
                website_url,
                checked_at,
                status,
                response_time,
                http_status_code,
                attempts
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            website_url,
            checked_at,
            status,
            response_time,
            http_status_code,
            attempts
        ))