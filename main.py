import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from models.house import add_house, view_houses, update_house_rent, delete_house
from models.tenant import add_tenant, view_tenants, delete_tenant
from models.payment import record_payment_by_name, view_all_payments
from utils.db import init_db, connect
from utils.receipt import generate_receipt
from datetime import datetime

USERNAME = "Admin"
PASSWORD = "AdminHouses"

class RentalSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Rental System")
        self.root.geometry("600x500")
        init_db()
        self.setup_ui()

    def setup_ui(self):
        # Main Frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=20)

        # Title
        tk.Label(main_frame, text="APPARTEMENT RENTAL SYSTEM", 
                font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=20)

        # Buttons
        buttons = [
            ("Add Appartement", self.gui_add_appartement),
            ("View Appartements", self.gui_view_appartements),
            ("Add Tenant", self.gui_add_tenant),
            ("View Tenants", self.gui_view_tenants),
            ("Record Payment", self.gui_record_payment),
            ("View All Payments", self.gui_view_payments),
            ("Manage Appartements", self.gui_manage_appartements),
            ("Manage Tenants", self.gui_manage_tenants),
            ("Check Overdue Rents", self.check_overdue_rents),
            ("Exit", self.root.destroy)
        ]

        for i, (text, command) in enumerate(buttons):
            tk.Button(main_frame, text=text, command=command, 
                     width=25, height=2).grid(row=(i//2)+1, column=i%2, padx=5, pady=5)

    # Appartement Management (original wording kept)
    def gui_add_appartement(self):
        appartement_number = simpledialog.askstring("Add Appartement", "Enter Appartement Number:")
        location = simpledialog.askstring("Add Appartement", "Enter Location:")
        rent_input = simpledialog.askstring("Add Appartement", "Enter Monthly Rent (KES):")

        try:
            rent = float(rent_input)
            add_house(appartement_number, location, rent)
            messagebox.showinfo("Success", "Appartement added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid rent amount.")

    def gui_view_appartements(self):
        appartements = view_houses()
        if not appartements:
            messagebox.showinfo("Appartements", "No appartements found.")
            return

        top = tk.Toplevel()
        top.title("All Appartements")
        
        tree = ttk.Treeview(top, columns=("ID", "Number", "Location", "Rent", "Status"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Number", text="Appartement No.")
        tree.heading("Location", text="Location")
        tree.heading("Rent", text="Rent (KES)")
        tree.heading("Status", text="Status")
        
        for app in appartements:
            tree.insert("", "end", values=app)
        
        tree.pack(fill="both", expand=True)

    # Tenant Management (original wording kept)
    def gui_add_tenant(self):
        appartements = view_houses()
        if not appartements:
            messagebox.showerror("Error", "No appartements available. Add appartements first.")
            return

        # Show available appartements
        app_list = "\n".join([f"{a[0]}: {a[1]} (KES {a[3]})" for a in appartements])
        house_id = simpledialog.askinteger("Add Tenant", f"Available Appartements:\n{app_list}\n\nEnter Appartement ID:")

        if house_id not in [a[0] for a in appartements]:
            messagebox.showerror("Error", "Invalid Appartement ID")
            return

        name = simpledialog.askstring("Add Tenant", "Enter Tenant Name:")
        phone = simpledialog.askstring("Add Tenant", "Enter Phone Number:")

        try:
            add_tenant(name, phone, house_id)
            messagebox.showinfo("Success", "Tenant added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add tenant: {str(e)}")

    def gui_view_tenants(self):
        tenants = view_tenants()
        if not tenants:
            messagebox.showinfo("Tenants", "No tenants found.")
            return

        top = tk.Toplevel()
        top.title("All Tenants")
        
        tree = ttk.Treeview(top, columns=("ID", "Name", "Phone", "Appartement", "Rent"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Phone", text="Phone")
        tree.heading("Appartement", text="Appartement")
        tree.heading("Rent", text="Rent (KES)")
        
        for tenant in tenants:
            tree.insert("", "end", values=tenant)
        
        tree.pack(fill="both", expand=True)

    # Payment Management (original wording kept)
    def gui_record_payment(self):
        tenant_name = simpledialog.askstring("Record Payment", "Enter Tenant Name:")
        if not tenant_name:
            return

        conn = connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT tenants.id, tenants.name, houses.house_number, houses.rent 
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
            options = "\n".join([f"{r[0]} - {r[1]} (Appartement {r[2]})" for r in results])
            chosen_id = simpledialog.askinteger("Multiple Matches", 
                                              f"Multiple tenants found:\n{options}\n\nEnter Tenant ID:")
            if not chosen_id:
                return
            match = next((r for r in results if r[0] == chosen_id), None)
        else:
            match = results[0]
        
        if not match:
            messagebox.showerror("Error", "Invalid selection.")
            return

        tenant_id, tenant_name, app_number, rent_amount = match
        amount = simpledialog.askfloat("Record Payment", 
                                     f"Enter Amount Paid for {tenant_name} (KES {rent_amount:.2f}):")
        if not amount:
            return

        try:
            record_payment_by_name(tenant_name, amount)
            receipt_id = f"{tenant_id}-{datetime.now().strftime('%Y%m%d')}"
            generate_receipt(tenant_name, app_number, amount, receipt_id)
            messagebox.showinfo("Success", f"Payment recorded!\nReceipt ID: {receipt_id}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to record payment: {str(e)}")

    def gui_view_payments(self):
        payments = view_all_payments()
        if not payments:
            messagebox.showinfo("Payments", "No payments found.")
            return

        top = tk.Toplevel()
        top.title("Payment History")
        
        tree = ttk.Treeview(top, columns=("ID", "Tenant", "Appartement", "Amount", "Date"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Tenant", text="Tenant")
        tree.heading("Appartement", text="Appartement")
        tree.heading("Amount", text="Amount (KES)")
        tree.heading("Date", text="Date")
        
        for p in payments:
            tree.insert("", "end", values=p)
        
        tree.pack(fill="both", expand=True)

    # Enhanced Management Features (with original wording)
    def gui_manage_appartements(self):
        appartements = view_houses()
        if not appartements:
            messagebox.showinfo("Appartements", "No appartements to manage.")
            return

        top = tk.Toplevel()
        top.title("Manage Appartements")
        
        tree = ttk.Treeview(top, columns=("ID", "Number", "Location", "Rent"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Number", text="Number")
        tree.heading("Location", text="Location")
        tree.heading("Rent", text="Rent (KES)")
        
        for app in appartements:
            tree.insert("", "end", values=app)
        
        tree.pack(fill="both", expand=True)

        # Management buttons
        btn_frame = tk.Frame(top)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Update Rent", 
                 command=lambda: self.update_appartement_rent(tree)).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Delete Appartement", 
                 command=lambda: self.delete_appartement(tree)).pack(side="left", padx=5)

    def update_appartement_rent(self, tree):
        selected = tree.focus()
        if not selected:
            messagebox.showerror("Error", "No appartement selected!")
            return

        item = tree.item(selected)
        app_id, number, location, rent = item['values']
        
        new_rent = simpledialog.askfloat("Update Rent", 
                                        f"Current rent: KES {rent}\nEnter new rent:",
                                        minvalue=0)
        if new_rent is None:
            return

        try:
            update_house_rent(app_id, new_rent)
            tree.item(selected, values=(app_id, number, location, new_rent))
            messagebox.showinfo("Success", "Rent updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update rent: {str(e)}")

    def delete_appartement(self, tree):
        selected = tree.focus()
        if not selected:
            messagebox.showerror("Error", "No appartement selected!")
            return

        item = tree.item(selected)
        app_id, number, *_ = item['values']
        
        confirm = messagebox.askyesno("Confirm Delete", 
                                    f"Delete appartement {number}?\nThis will also remove associated tenants!")
        if not confirm:
            return

        try:
            delete_house(app_id)
            tree.delete(selected)
            messagebox.showinfo("Success", "Appartement deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete appartement: {str(e)}")

    def gui_manage_tenants(self):
        tenants = view_tenants()
        if not tenants:
            messagebox.showinfo("Tenants", "No tenants to manage.")
            return

        top = tk.Toplevel()
        top.title("Manage Tenants")
        
        tree = ttk.Treeview(top, columns=("ID", "Name", "Phone", "Appartement"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Phone", text="Phone")
        tree.heading("Appartement", text="Appartement")
        
        for tenant in tenants:
            tree.insert("", "end", values=tenant[:4])  # Exclude rent from display
        
        tree.pack(fill="both", expand=True)

        tk.Button(top, text="Delete Tenant", 
                 command=lambda: self.delete_tenant_from_system(tree)).pack(pady=10)

    def delete_tenant_from_system(self, tree):
        selected = tree.focus()
        if not selected:
            messagebox.showerror("Error", "No tenant selected!")
            return

        item = tree.item(selected)
        tenant_id, name, *_ = item['values']
        
        confirm = messagebox.askyesno("Confirm Delete", f"Delete tenant {name}?")
        if not confirm:
            return

        try:
            delete_tenant(tenant_id)
            tree.delete(selected)
            messagebox.showinfo("Success", "Tenant deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete tenant: {str(e)}")

    # Overdue Rent Checker (original wording kept)
    def check_overdue_rents(self):
        conn = connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT t.name, h.house_number, p.payment_date 
            FROM tenants t
            JOIN houses h ON t.house_id = h.id
            LEFT JOIN payments p ON t.name = p.tenant_name 
            AND strftime('%Y-%m', p.payment_date) = strftime('%Y-%m', 'now')
            WHERE p.id IS NULL
        """)
        overdue_tenants = cur.fetchall()
        conn.close()

        if not overdue_tenants:
            messagebox.showinfo("Rent Status", "All rents are paid for this month!")
            return

        output = "Tenants with overdue rent:\n\n"
        for tenant in overdue_tenants:
            output += f"{tenant[0]} (Appartement {tenant[1]})\n"

        messagebox.showwarning("Overdue Rents", output)

    def run(self):
        self.root.mainloop()

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
        if username_entry.get() == USERNAME and password_entry.get() == PASSWORD:
            login_window.destroy()
            app = RentalSystem()
            app.run()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    tk.Button(login_window, text="Login", command=attempt_login, bg="green", fg="white").pack(pady=20)
    login_window.mainloop()

if __name__ == "__main__":
    init_db()
    show_login()