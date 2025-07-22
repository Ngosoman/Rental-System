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
    print("✅ Payment recorded successfully.")
