import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import subprocess
class ViewDataPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventory Data Viewer")
        self.geometry("1000x500")

        # Check if the database exists
        db_path = 'inventory.db'
        if not os.path.exists(db_path):
            messagebox.showerror("Database Error", "Database file 'inventory.db' not found.")
            self.destroy()
            return

        # Connect to the database
        try:
            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {e}")
            self.destroy()
            return

        # Create tabbed interface
        tab_control = ttk.Notebook(self)

        # Imports Tab
        imports_tab = ttk.Frame(tab_control)
        tab_control.add(imports_tab, text='Imports')
        self.display_data(imports_tab, "imports1")

        # Exports Tab
        exports_tab = ttk.Frame(tab_control)
        tab_control.add(exports_tab, text='Exports')
        self.display_data(exports_tab, "exports1")

        tab_control.pack(expand=1, fill='both')

        # 🔙 Back to Home Button
        tk.Button(self, text="Back to Home", command=self.go_back_home).pack(pady=10)

    def display_data(self, tab, table_name):
        # Define columns
        if table_name == "imports1":
            columns = ("ID", "Supplier ID", "Supplier Name", "Date", "Quantity", "Price per Unit", "Total Cost")
        elif table_name == "exports1":
            columns = ("ID", "Exporter ID", "Exporter Name", "Date", "Quantity", "Price per Unit", "Total Revenue")

        # Treeview widget
        tree = ttk.Treeview(tab, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=120)

        # Add vertical scrollbar
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(expand=True, fill='both')

        # Fetch and insert data
        try:
            self.cursor.execute(f"SELECT * FROM {table_name}")
            rows = self.cursor.fetchall()
            if rows:
                for row in rows:
                    tree.insert("", tk.END, values=row)
                if table_name == "imports1":
                    self.cursor.execute(f"SELECT SUM(total_cost) FROM {table_name}")
                    totalcost = self.cursor.fetchone()[0]

                    # Add the total cost value at the bottom
                    total_cost_label = tk.Label(tab, text=f"Total Cost: {totalcost}", font=("Arial", 10, "bold"))
                    total_cost_label.pack(side=tk.BOTTOM, padx=10, pady=10)
                elif table_name == "exports1":
                    self.cursor.execute(f"SELECT SUM(total_revenue) FROM {table_name}")
                    totalcost = self.cursor.fetchone()[0]

                    # Add the total cost value at the bottom
                    total_cost_label = tk.Label(tab, text=f"Total Revenue: {totalcost}", font=("Arial", 10, "bold"))
                    total_cost_label.pack(side=tk.BOTTOM, padx=10, pady=10)
            else:
                messagebox.showinfo("No Data", f"No data found in {table_name} table.")
        except sqlite3.OperationalError as e:
            messagebox.showerror("Error", f"Table '{table_name}' not found. Please check your database.\nError: {e}")

    def go_back_home(self):
        """Close the current window and return to the home screen."""
        self.destroy()  # Close the import window
        subprocess.Popen(["python", "homepage.py"])  # Open the homepage
if __name__ == "__main__":
    app = ViewDataPage()
    app.mainloop()