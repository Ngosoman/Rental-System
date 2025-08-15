import tkinter as tk
from tkinter import messagebox
from database import Tenant

def check_overdue_rents():
    # Fetch tenants with unpaid rent (modify query as needed)
    overdue_tenants = Tenant.select().where(Tenant.paid_status == False)
    
    if overdue_tenants:
        root = tk.Tk()
        root.withdraw()  # Hide main window
        for tenant in overdue_tenants:
            messagebox.showwarning(
                "RENT OVERDUE",
                f"{tenant.name} in House {tenant.house.name}\nDue Date: {tenant.due_date}"
            )
        root.destroy()
    else:
        print("No overdue rents found.")

if __name__ == "__main__":
    check_overdue_rents()  # Run manually or via scheduler