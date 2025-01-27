import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime

# --- Database Setup ---
conn = sqlite3.connect("pepper_inventory.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS imports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    quantity INTEGER,
    price_per_unit REAL,
    total_cost REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS exports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    quantity INTEGER,
    price_per_unit REAL,
    total_revenue REAL
)
""")

conn.commit()

# --- Functions to Add and View Data ---
def add_import():
    try:
        qty = int(import_quantity_entry.get())
        price = float(import_price_entry.get())
        total_cost = qty * price
        cursor.execute("INSERT INTO imports (date, quantity, price_per_unit, total_cost) VALUES (?, ?, ?, ?)",
                       (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), qty, price, total_cost))
        conn.commit()
        messagebox.showinfo("Success", "Import data added successfully!")
        view_imports()  # Refresh view

        # Clear input fields
        import_quantity_entry.delete(0, tk.END)
        import_price_entry.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for quantity and price.")

def add_export():
    try:
        qty = int(export_quantity_entry.get())
        price = float(export_price_entry.get())
        total_revenue = qty * price
        cursor.execute("INSERT INTO exports (date, quantity, price_per_unit, total_revenue) VALUES (?, ?, ?, ?)",
                       (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), qty, price, total_revenue))
        conn.commit()
        messagebox.showinfo("Success", "Export data added successfully!")
        view_exports()  # Refresh view

        # Clear input fields
        export_quantity_entry.delete(0, tk.END)
        export_price_entry.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for quantity and price.")
def view_imports():
    for row in import_table.get_children():
        import_table.delete(row)
    cursor.execute("SELECT * FROM imports")
    for row in cursor.fetchall():
        import_table.insert('', tk.END, values=row)

def view_exports():
    for row in export_table.get_children():
        export_table.delete(row)
    cursor.execute("SELECT * FROM exports")
    for row in cursor.fetchall():
        export_table.insert('', tk.END, values=row)

def view_inventory():
    total_imports = cursor.execute("SELECT SUM(quantity) FROM imports").fetchone()[0] or 0
    total_exports = cursor.execute("SELECT SUM(quantity) FROM exports").fetchone()[0] or 0
    current_stock = total_imports - total_exports

    inventory_label.config(text=f"Current Pepper Stock: {current_stock} kg")

def clear_database():
    confirm = messagebox.askyesno("Confirm", "Are you sure you want to clear all data?")
    if confirm:
        cursor.execute("DELETE FROM imports")
        cursor.execute("DELETE FROM exports")
        conn.commit()
        messagebox.showinfo("Success", "All data has been cleared!")
        view_imports()
        view_exports()
# --- GUI Setup ---
root = tk.Tk()
root.title("Pepper Inventory Management System")
root.geometry("700x500")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# --- Imports Tab ---
import_frame = tk.Frame(notebook)
notebook.add(import_frame, text="Imports")

tk.Label(import_frame, text="Quantity (kg):").pack()
import_quantity_entry = tk.Entry(import_frame)
import_quantity_entry.pack()

tk.Label(import_frame, text="Price per kg:").pack()
import_price_entry = tk.Entry(import_frame)
import_price_entry.pack()

tk.Button(import_frame, text="Add Import", command=add_import).pack(pady=5)
tk.Button(import_frame, text="View Imports", command=view_imports).pack(pady=5)
clear_button = tk.Button(root, text="Clear Database", command=clear_database)
clear_button.pack(pady=10)
# Table for Imports
import_table = ttk.Treeview(import_frame, columns=("ID", "Date", "Quantity", "Price/Unit", "Total Cost"), show="headings")
for col in ("ID", "Date", "Quantity", "Price/Unit", "Total Cost"):
    import_table.heading(col, text=col)
    import_table.column(col, width=100)
import_table.pack(expand=True, fill="both")

# --- Exports Tab ---
export_frame = tk.Frame(notebook)
notebook.add(export_frame, text="Exports")

tk.Label(export_frame, text="Quantity (kg):").pack()
export_quantity_entry = tk.Entry(export_frame)
export_quantity_entry.pack()

tk.Label(export_frame, text="Price per kg:").pack()
export_price_entry = tk.Entry(export_frame)
export_price_entry.pack()

tk.Button(export_frame, text="Add Export", command=add_export).pack(pady=5)
tk.Button(export_frame, text="View Exports", command=view_exports).pack(pady=5)

# Table for Exports
export_table = ttk.Treeview(export_frame, columns=("ID", "Date", "Quantity", "Price/Unit", "Total Revenue"), show="headings")
for col in ("ID", "Date", "Quantity", "Price/Unit", "Total Revenue"):
    export_table.heading(col, text=col)
    export_table.column(col, width=100)
export_table.pack(expand=True, fill="both")

# --- Inventory Tab ---
inventory_frame = tk.Frame(notebook)
notebook.add(inventory_frame, text="Current Inventory")

inventory_label = tk.Label(inventory_frame, text="Current Pepper Stock: 0 kg", font=("Helvetica", 16))
inventory_label.pack(pady=20)

tk.Button(inventory_frame, text="Refresh Inventory", command=view_inventory).pack(pady=5)

# --- Start the App ---
root.mainloop()