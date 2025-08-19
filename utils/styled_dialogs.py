import tkinter as tk
from tkinter import ttk
from styles import configure_styles, PRIMARY_COLOR, WHITE

def create_styled_messagebox(title, message, message_type="info"):
    """Create a styled message box"""
    dialog = tk.Toplevel()
    dialog.title(title)
    dialog.configure(bg="#ecf0f1")
    dialog.transient(dialog.master)
    dialog.grab_set()
    
    ttk.Label(dialog, text=message, style="TLabel").pack(padx=20, pady=20)
    ttk.Button(dialog, text="OK", command=dialog.destroy, style="Primary.TButton").pack(pady=10)
    
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
    y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
    dialog.geometry(f"+{x}+{y}")
    
    return dialog