import sqlite3
import os

DB_PATH = os.path.join("data", "rental.db")

def connect():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS houses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            house_number TEXT NOT NULL,
            location TEXT NOT NULL,
            rent_amount REAL NOT NULL
        )
    ''')

    