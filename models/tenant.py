from utils.db import connect

def add_tenant(name, phone, house_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO tenants (name, phone, house_id) VALUES (?, ?, ?)",
                (name, phone, house_id))
    conn.commit()
    conn.close()
    print("Tenant added successfully.")

def view_tenants():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT tenants.id, tenants.name, tenants.phone, houses.house_number
        FROM tenants
        JOIN houses ON tenants.house_id = houses.id
    """)
    tenants = cur.fetchall()
    conn.close()

    if tenants:
        for tenant in tenants:
            print(f"ID: {tenant[0]} | Name: {tenant[1]} | Phone: {tenant[2]} | House: {tenant[3]}")
    else:
        print("No tenants found.")
