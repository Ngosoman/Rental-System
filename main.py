import tkinter as tk
from tkinter import messagebox, simpledialog
from models.house import add_house, view_houses
from models.tenant import add_tenant, view_tenants
from models.payment import record_payment_by_name, view_all_payments
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
    if tenants:
        output = "\n".join([f"{t[0]} | {t[1]} | {t[2]} | {t[3]}" for t in tenants])
    else:
        output = "No tenants found."

    messagebox.showinfo("Tenants", output)

def gui_record_payment():
    tenant_name = simpledialog.askstring("Record Payment", "Enter Tenant Name:")
    amount_input = simpledialog.askstring("Record Payment", "Enter Amount Paid (KES):")
    
    try:
        amount = float(amount_input)

        conn = connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT tenants.id, tenants.name, houses.house_number 
            FROM tenants 
            JOIN houses ON tenants.house_id = houses.id 
            WHERE tenants.name LIKE ?
        """, (f"%{tenant_name}%",))
        results = cur.fetchall()
        conn.close()

        if not results:
            messagebox.showerror("Error", "No tenant found with that name.")
            return
        
        if len(results) > 1:
            options = "\n".join([f"{r[0]} - {r[1]} (House {r[2]})" for r in results])
            chosen_id = simpledialog.askinteger("Multiple Matches Found",
                                                 f"Multiple tenants match.\nSelect Tenant ID:\n{options}")
            match = next((r for r in results if r[0] == chosen_id), None)
        else:
            match = results[0]
        
        if match:
            tenant_id, tenant_name, house_number = match
            record_payment_by_name("John Doe", 8500)
            receipt_id = tenant_id * 1000 + int(amount)
            generate_receipt(tenant_name, house_number, amount, receipt_id)
            messagebox.showinfo("Success", "Payment recorded and receipt generated.")
        else:
            messagebox.showerror("Error", "Selected tenant ID not valid.")
            
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
