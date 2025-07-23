from utils.db import connect
from datetime import datetime

def record_payment(tenant_id, amount):
    conn = connect()
    cur = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("INSERT INTO payments (tenant_id, amount_paid, date) VALUES (?, ?, ?)",
                (tenant_id, amount, date))
    conn.commit()
    conn.close()
    print("Payment recorded successfully.")


def view_all_payments():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT payments.id, tenants.name, houses.house_number, payments.amount, payments.date_paid
        FROM payments
        JOIN tenants ON payments.tenant_id = tenants.id
        JOIN houses ON tenants.house_id = houses.id
        ORDER BY payments.date_paid DESC
    """)

    rows = cur.fetchall()
    conn.close()

    print("\n ALL RENT PAYMENTS")
    print("-" * 50)
    for row in rows:
        print(f"ReceiptID: {row[0]} | Tenant: {row[1]} | House: {row[2]} | Amount: KES {row[3]} | Date: {row[4]}")
    print("-" * 50)

