from utils.db import connect

def add_house(house_number, location, rent_amount):
    """Add a new house to the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO houses (house_number, location, rent_amount) VALUES (?, ?, ?)",
        (house_number, location, rent_amount)
    )
    conn.commit()
    conn.close()
    print(f" House '{house_number}' in '{location}' added successfully at KES {rent_amount:.2f} per month.")

def view_houses():
    """Fetch and display all houses from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, house_number, location, rent_amount FROM houses")
    houses = cur.fetchall()
    conn.close()

    if not houses:
        print(" No houses found.")
    else:
        print("\n Available Houses:")
        print("-" * 50)
        for house in houses:
            house_id, house_number, location, rent_amount = house
            print(f"ID: {house_id} | Number: {house_number} | Location: {location} | Rent: KES {rent_amount:.2f}")
        print("-" * 50)

    return houses
