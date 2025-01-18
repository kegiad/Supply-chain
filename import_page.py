import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess  # To open the homepage

class ImportPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Add Imports")
        self.geometry("400x400")

        # Supplier ID
        tk.Label(self, text="Supplier ID:").pack()
        self.supplier_id_entry = tk.Entry(self)
        self.supplier_id_entry.pack()

        # Supplier Name
        tk.Label(self, text="Supplier Name:").pack()
        self.supplier_name_entry = tk.Entry(self)
        self.supplier_name_entry.pack()

        # Quantity
        tk.Label(self, text="Quantity (kg):").pack()
        self.quantity_entry = tk.Entry(self)
        self.quantity_entry.pack()

        # Price Per Unit
        tk.Label(self, text="Price per Unit (₹):").pack()
        self.price_entry = tk.Entry(self)
        self.price_entry.pack()

        # Add Import Button
        tk.Button(self, text="Add Import", command=self.add_import).pack(pady=10)

        # 🔙 Back to Home Button
        tk.Button(self, text="Back to Home", command=self.go_back_home).pack(pady=10)

    def add_import(self):
        supplier_id = self.supplier_id_entry.get()
        supplier_name = self.supplier_name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()

        if not (supplier_id and supplier_name and quantity and price):
            messagebox.showwarning("Input Error", "All fields must be filled.")
            return

        try:
            quantity = int(quantity)
            price = float(price)
            total_cost = quantity * price

            conn = sqlite3.connect('inventory.db')
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO imports1 (supplier_id, supplier_name, date, quantity, price_per_unit, total_cost)
                VALUES (?, ?, date('now'), ?, ?, ?)
            """, (supplier_id, supplier_name, quantity, price, total_cost))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Import added successfully!")
            self.clear_fields()

        except ValueError:
            messagebox.showerror("Input Error", "Quantity and Price must be numbers.")

    def clear_fields(self):
        self.supplier_id_entry.delete(0, tk.END)
        self.supplier_name_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

    def go_back_home(self):
        """Close the current window and return to the home screen."""
        self.destroy()  # Close the import window
        subprocess.Popen(["python", "homepage.py"])  # Open the homepage

if __name__ == "__main__":
    app = ImportPage()
    app.mainloop()