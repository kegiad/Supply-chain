import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess  # To open the homepage

class ImportPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Add Imports")
        self.geometry("400x400")

        # Constants
        self.MAX_CAPACITY = 10000  # Maximum storage capacity in kg

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

        # Back to Home Button
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

            if quantity <= 0 or price <= 0:
                messagebox.showerror("Input Error", "Quantity and Price must be positive numbers.")
                return

            # Check inventory capacity
            current_inventory = self.get_current_inventory()
            if current_inventory + quantity > self.MAX_CAPACITY:
                messagebox.showerror(
                    "Capacity Exceeded",
                    f"Adding {quantity} kg will exceed the maximum capacity of {self.MAX_CAPACITY} kg.\n"
                    f"Current Inventory: {current_inventory} kg"
                )
                return

            # Calculate total cost
            total_cost = quantity * price

            # Add to database
            conn = sqlite3.connect('inventory.db')
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO imports1 (supplier_id, supplier_name, date, quantity, price_per_unit, total_cost)
                VALUES (?, ?, date('now'), ?, ?, ?)
            """, (supplier_id, supplier_name, quantity, price, total_cost))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", f"Successfully imported {quantity} kg!")
            self.clear_fields()

        except ValueError:
            messagebox.showerror("Input Error", "Quantity and Price must be valid numbers.")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def get_current_inventory(self):
        """Fetch the current inventory level from the database."""
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()

        try:
            # Calculate total imports and exports
            cursor.execute("SELECT SUM(quantity) FROM imports1")
            total_imports = cursor.fetchone()[0] or 0

            cursor.execute("SELECT SUM(quantity) FROM exports1")
            total_exports = cursor.fetchone()[0] or 0

            return total_imports - total_exports

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred while fetching inventory: {e}")
            return 0

        finally:
            conn.close()

    def clear_fields(self):
        """Clear all input fields."""
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