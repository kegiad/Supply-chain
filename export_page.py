import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess  # To open the homepage

class ExportPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Add Exports")
        self.geometry("400x400")

        # Exporter ID
        tk.Label(self, text="Exporter ID:").pack()
        self.exporter_id_entry = tk.Entry(self)
        self.exporter_id_entry.pack()

        # Exporter Name
        tk.Label(self, text="Exporter Name:").pack()
        self.exporter_name_entry = tk.Entry(self)
        self.exporter_name_entry.pack()

        # Quantity
        tk.Label(self, text="Quantity (kg):").pack()
        self.quantity_entry = tk.Entry(self)
        self.quantity_entry.pack()

        # Price Per Unit
        tk.Label(self, text="Price per Unit (₹):").pack()
        self.price_entry = tk.Entry(self)
        self.price_entry.pack()

        # Add Export Button
        tk.Button(self, text="Add Export", command=self.add_export).pack(pady=10)

        # 🔙 Back to Home Button
        tk.Button(self, text="Back to Home", command=self.go_back_home).pack(pady=10)

    def add_export(self):
        exporter_id = self.exporter_id_entry.get()
        exporter_name = self.exporter_name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()

        if not (exporter_id and exporter_name and quantity and price):
            messagebox.showwarning("Input Error", "All fields must be filled.")
            return

        try:
            quantity = int(quantity)
            price = float(price)

            if quantity <= 0 or price <= 0:
                messagebox.showerror("Input Error", "Quantity and Price must be positive numbers.")
                return

            # Check inventory availability
            current_inventory = self.get_current_inventory()
            if quantity > current_inventory:
                messagebox.showerror(
                    "Insufficient Inventory",
                    "There is not enough pepper in the inventory to export this much."
                )
                return

            # Calculate total revenue
            total_revenue = quantity * price

            # Add to database
            conn = sqlite3.connect('inventory.db')
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO exports1 (exporter_id, exporter_name, date, quantity, price_per_unit, total_revenue)
                VALUES (?, ?, date('now'), ?, ?, ?)
            """, (exporter_id, exporter_name, quantity, price, total_revenue))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", f"Successfully exported {quantity} kg!")
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
        self.exporter_id_entry.delete(0, tk.END)
        self.exporter_name_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

    def go_back_home(self):
        """Close the current window and return to the home screen."""
        self.destroy()  # Close the export window
        subprocess.Popen(["python", "homepage.py"])  # Open the homepage


if __name__ == "__main__":
    app = ExportPage()
    app.mainloop()