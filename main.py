from utils.db import init_db
from models.house import add_house, view_houses
from models.tenant import add_tenant, view_tenants

def menu():
    print("""
    === Rental House Management ===
    1. Add House
    2. View Houses
    3. Add Tenant
    4. View Tenants
    0. Exit
    """)

def main():
    init_db()

    while True:
        menu()
        choice = input("Enter choice: ")

        if choice == "1":
            num = input("House number: ")
            loc = input("Location: ")
            rent = float(input("Rent amount: "))
            add_house(num, loc, rent)

        elif choice == "2":
            for h in view_houses():
                print(h)

        elif choice == "3":
            name = input("Tenant name: ")
            phone = input("Phone: ")
            hid = int(input("House ID: "))
            add_tenant(name, phone, hid)

        elif choice == "4":
            for t in view_tenants():
                print(t)

        elif choice == "0":
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
