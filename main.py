import tkinter as tk
from tkinter import messagebox, simpledialog
from models.house import add_house, view_houses
from models.tenant import add_tenant, view_tenants
from models.payment import record_payment_by_name, view_all_payments
from utils.db import init_db, connect
from utils.receipt import generate_receipt

USERNAME = "Admin"
PASSWORD = "AdminHouses"

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
            record_payment_by_name(tenant_name, amount)
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
        output = ""
        for p in payments:
            pay_id = p[0]
            tenant = p[1]
            house = p[2]
            amount = float(p[3])
            date = str(p[4]) 
            output += f"ID: {pay_id} | Tenant: {tenant} | House: {house} | Amount: KES {amount:.2f} | Date: {date}\n"
        messagebox.showinfo("All Payments", output)

def show_main_window():
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

def show_login():
    login_window = tk.Tk()
    login_window.title("Admin Login")
    login_window.geometry("300x200")

    tk.Label(login_window, text="Username").pack(pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    tk.Label(login_window, text="Password").pack(pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()

        if username == USERNAME and password == PASSWORD:
            login_window.destroy()
            show_main_window()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")

    tk.Button(login_window, text="Login", command=attempt_login, bg="green", fg="white").pack(pady=10)
    login_window.mainloop()

def main():
    init_db()
    show_login()

if __name__ == "__main__":
    main()
