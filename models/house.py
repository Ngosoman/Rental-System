from utils.db import connect

def add_house(house_number, location, rent_amount):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO houses (house_number, location, rent_amount) VALUES (?, ?, ?)",
                (house_number, location, rent_amount))
    conn.commit()
    conn.close()
    print("✅ House added successfully.")

def view_houses():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM houses")
    houses = cur.fetchall()
    conn.close()
    return houses
