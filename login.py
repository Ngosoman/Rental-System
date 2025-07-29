import tkinter as tk
from tkinter import messagebox
from main import main_window 

def login():
    username = entry_username.get()
    password = entry_password.get()

    if username == "Admin" and password == "AdminHouses":
        root.destroy() 
        main_window()   
    else:
        messagebox.showerror("Login Failed", "Invalid credentials!")

# Login Window
root = tk.Tk()
root.title("Admin Login")
root.geometry("300x200")
root.configure(bg="white")

tk.Label(root, text="Username", bg="white").pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

tk.Label(root, text="Password", bg="white").pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

tk.Button(root, text="Login", command=login, bg="black", fg="white").pack(pady=20)

root.mainloop()
