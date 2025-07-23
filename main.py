from models.house import add_house, view_houses
from models.tenant import add_tenant, view_tenants
from models.payment import record_payment
from utils.db import init_db, connect
from utils.reciept import generate_receipt

def main():
    init_db()
    while True:
        print("\nRENTAL HOUSE MANAGEMENT SYSTEM")
        print("1. Add House")
        print("2. View Houses")
        print("3. Add Tenant")
        print("4. View Tenants")
        print("5. Record Payment")
        print("6. View All Payments")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            house_number = input("House Number: ")
            rent = float(input("Monthly Rent: "))
            add_house(house_number, rent)

        elif choice == "2":
            view_houses()

        elif choice == "3":
            name = input("Tenant Name: ")
            phone = input("Phone Number: ")
            house_id = int(input("House ID: "))
            add_tenant(name, phone, house_id)

        elif choice == "4":
            view_tenants()

        elif choice == "5":
            tid = int(input("Tenant ID: "))
            amount = float(input("Amount Paid (KES): "))

            # Tenant  Info
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
                tenant_name, house_number = result
                record_payment(tid, amount)
                receipt_id = tid * 1000 + int(amount) 
                generate_receipt(tenant_name, house_number, amount, receipt_id)
            else:
                print("Tenant not found.")

        elif choice == "6":
            from models.payment import view_all_payments
            view_all_payments()


        elif choice == "7":
            print(" Exiting system. Goodbye!")
            break

        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
