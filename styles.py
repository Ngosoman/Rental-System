import tkinter as tk
from tkinter import ttk

# Color scheme
PRIMARY_COLOR = "#2c3e50"      # Dark blue
SECONDARY_COLOR = "#3498db"    # Blue
ACCENT_COLOR = "#e74c3c"       # Red
SUCCESS_COLOR = "#27ae60"      # Green
WARNING_COLOR = "#f39c12"      # Orange
LIGHT_BG = "#ecf0f1"           # Light gray
DARK_TEXT = "#2c3e50"          # Dark text
WHITE = "#ffffff"              # White

# Fonts
TITLE_FONT = ("Arial", 18, "bold")
HEADING_FONT = ("Arial", 14, "bold")
BUTTON_FONT = ("Arial", 10, "bold")
TEXT_FONT = ("Arial", 10)
SMALL_FONT = ("Arial", 9)

def configure_styles():
    """Configure ttk styles for the application"""
    style = ttk.Style()
    
    # Configure main styles
    style.configure("TFrame", background=LIGHT_BG)
    style.configure("TLabel", background=LIGHT_BG, font=TEXT_FONT)
    style.configure("Title.TLabel", font=TITLE_FONT, foreground=PRIMARY_COLOR)
    style.configure("Heading.TLabel", font=HEADING_FONT, foreground=PRIMARY_COLOR)
    
    # Button styles
    style.configure("Primary.TButton", 
                   font=BUTTON_FONT,
                   background=PRIMARY_COLOR,
                   foreground=WHITE,
                   padding=10,
                   focuscolor=SECONDARY_COLOR)
    
    style.configure("Secondary.TButton",
                   font=BUTTON_FONT,
                   background=SECONDARY_COLOR,
                   foreground=WHITE,
                   padding=10)
    
    style.configure("Success.TButton",
                   font=BUTTON_FONT,
                   background=SUCCESS_COLOR,
                   foreground=WHITE,
                   padding=10)
    
    style.configure("Warning.TButton",
                   font=BUTTON_FONT,
                   background=WARNING_COLOR,
                   foreground=WHITE,
                   padding=10)
    
    style.configure("Danger.TButton",
                   font=BUTTON_FONT,
                   background=ACCENT_COLOR,
                   foreground=WHITE,
                   padding=10)
    
    # Entry styles
    style.configure("TEntry", 
                   font=TEXT_FONT,
                   padding=5,
                   fieldbackground=WHITE)
    
    # Treeview styles
    style.configure("Treeview",
                   font=TEXT_FONT,
                   background=WHITE,
                   fieldbackground=WHITE)
    
    style.configure("Treeview.Heading",
                   font=BUTTON_FONT,
                   background=PRIMARY_COLOR,
                   foreground=WHITE,
                   padding=5)
    
    style.map("Treeview.Heading",
             background=[('active', SECONDARY_COLOR)])
    
    # Notebook (tab) styles
    style.configure("TNotebook", background=LIGHT_BG)
    style.configure("TNotebook.Tab", 
                   font=BUTTON_FONT,
                   padding=10,
                   background=SECONDARY_COLOR,
                   foreground=WHITE)
    
    style.map("TNotebook.Tab",
             background=[('selected', PRIMARY_COLOR), ('active', SECONDARY_COLOR)])

def create_styled_button(parent, text, command, style="Primary.TButton"):
    """Create a styled button with consistent appearance"""
    button = ttk.Button(parent, text=text, command=command, style=style)
    return button

def create_styled_label(parent, text, style="TLabel"):
    """Create a styled label"""
    label = ttk.Label(parent, text=text, style=style)
    return label

def create_styled_entry(parent, width=20):
    """Create a styled entry field"""
    entry = ttk.Entry(parent, width=width, style="TEntry")
    return entry

def center_window(window):
    """Center the window on screen"""
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')