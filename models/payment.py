from utils.db import connect
from datetime import datetime
from utils.receipt import generate_receipt  

def record_payment_by_name(tenant_name, amount):
    conn = connect()
    cur = conn.cursor()

    # Lookup tenant ID and house number from name
    cur.execute("""
        SELECT tenants.id, houses.house_number 
        FROM tenants 
        JOIN houses ON tenants.house_id = houses.id 
        WHERE tenants.name = ?
    """, (tenant_name,))
    
    tenant = cur.fetchone()

    if tenant:
        tenant_id, house_number = tenant
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cur.execute("INSERT INTO payments (tenant_id, amount_paid, date) VALUES (?, ?, ?)",
                    (tenant_id, amount, date))

        receipt_id = cur.lastrowid
        conn.commit()
        conn.close()

        print("Payment recorded successfully.")
        generate_receipt(tenant_name, house_number, amount, receipt_id)

    else:
        conn.close()
        raise Exception("Tenant not found. Please check the name.")

def view_all_payments():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT payments.id, tenants.name, houses.house_number, payments.amount_paid, payments.date
        FROM payments
        JOIN tenants ON payments.tenant_id = tenants.id
        JOIN houses ON tenants.house_id = houses.id
        ORDER BY payments.date DESC
    """)

    rows = cur.fetchall()
    conn.close()

    print("\n ALL RENT PAYMENTS")
    print("-" * 80)
    for row in rows:
        print(f"ReceiptID: {row[0]} | Tenant: {row[1]} | House: {row[2]} | Amount: KES {row[3]} | Date: {row[4]}")
    print("-" * 80)
