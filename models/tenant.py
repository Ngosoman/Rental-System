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
    cur.execute("SELECT * FROM tenants")
    tenants = cur.fetchall()
    conn.close()
    return tenants
