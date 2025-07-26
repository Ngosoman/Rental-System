import tkinter as tk
from tkinter import messagebox, simpledialog
from models.house import add_house, view_houses
from models.tenant import add_tenant, view_tenants
from models.payment import record_payment, view_all_payments
from utils.db import init_db, connect
from utils.receipt import generate_receipt

def gui_add_appartement():
    appartement_number = simpledialog.askstring("Add Appartement", "Enter Appartement Number:")
    location = simpledialog.askstring("Add Appartement", "Enter Location:")
    rent_input = simpledialog.askstring("Add Appartement", "Enter Monthly Rent (KES):")

    try:
        rent = float(rent_input)
        add_house(appartement_number, location, rent)
        messagebox.showinfo("Success", "Appartement added successfully.")
    except:
        messagebox.showerror("Error", "Please enter a valid rent amount.")

def gui_view_appartements():
    appartements = view_houses()
    if not appartements:
        messagebox.showinfo("Appartements", "No appartements found.")
    else:
        output = "\n".join([f"{a[1]} | {a[2]} | KES {float(a[3]):,.2f}" for a in appartements])
        messagebox.showinfo("All Appartements", output)

def gui_add_tenant():
    name = simpledialog.askstring("Add Tenant", "Enter Tenant Name:")
    phone = simpledialog.askstring("Add Tenant", "Enter Phone Number:")
    appartement_id = simpledialog.askstring("Add Tenant", "Enter Appartement ID:")

    try:
        add_tenant(name, phone, int(appartement_id))
        messagebox.showinfo("Success", "Tenant added successfully.")
    except:
        messagebox.showerror("Error", "Failed to add tenant. Check input.")

def gui_view_tenants():
    tenants = view_tenants()
    if not tenants:
        messagebox.showinfo("Tenants", "No tenants found.")
    else:
        output = "\n".join([f"{t[0]} | {t[1]} | {t[2]} | Appartement #{t[3]}" for t in tenants])
        messagebox.showinfo("All Tenants", output)

def gui_record_payment():
    tid = simpledialog.askstring("Record Payment", "Enter Tenant ID:")
    amount_input = simpledialog.askstring("Record Payment", "Enter Amount Paid (KES):")
    try:
        tid = int(tid)
        amount = float(amount_input)

        conn = connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT tenants.name, houses.house_number 
            FROM tenants 
            JOIN houses ON tenants.house_id = houses.id 
            WHERE tenants.id = ?
        """, (tid,))
        result = cur.fetchone()
        conn.close()

        if result:
            tenant_name, appartement_number = result
            record_payment(tid, amount)

            receipt_id = tid * 1000 + int(amount)
            generate_receipt(tenant_name, appartement_number, amount, receipt_id)
            messagebox.showinfo("Success", "Payment recorded and receipt generated.")
        else:
            messagebox.showerror("Error", "Tenant not found.")
    except:
        messagebox.showerror("Error", "Invalid input.")

def gui_view_payments():
    payments = view_all_payments()
    if not payments:
        messagebox.showinfo("Payments", "No payments found.")
    else:
        output = "\n".join([f"{p[0]} | {p[1]} | {p[2]} | KES {p[3]}" for p in payments])
        messagebox.showinfo("All Payments", output)

def main():
    init_db()
    root = tk.Tk()
    root.title("Rent System")
    root.geometry("400x400")

    tk.Label(root, text="RENT SYSTEM", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Button(root, text="Add Appartement", command=gui_add_appartement, width=30).pack(pady=5)
    tk.Button(root, text="View Appartements", command=gui_view_appartements, width=30).pack(pady=5)
    tk.Button(root, text="Add Tenant", command=gui_add_tenant, width=30).pack(pady=5)
    tk.Button(root, text="View Tenants", command=gui_view_tenants, width=30).pack(pady=5)
    tk.Button(root, text="Record Payment", command=gui_record_payment, width=30).pack(pady=5)
    tk.Button(root, text="View All Payments", command=gui_view_payments, width=30).pack(pady=5)
    tk.Button(root, text="Exit", command=root.destroy, width=30, bg="red", fg="white").pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
