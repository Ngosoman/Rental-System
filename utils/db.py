import sqlite3
import os

DB_PATH = os.path.join("data", "rental.db")

def connect():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = connect()
    cursor = conn.cursor()