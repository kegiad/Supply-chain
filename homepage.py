import tkinter as tk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk
from import_page import ImportPage
from export_page import ExportPage
from inventory_viewer import ViewDataPage

class HomePage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pepper Inventory Management")
        self.geometry("800x600")

        # Create a canvas to hold the background image
        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Load the background image using Pillow (PIL)
        self.bg_image = Image.open("pepper.jpeg")  # Load your jpeg image
        self.bg_image = ImageTk.PhotoImage(self.bg_image)  # Convert to a Tkinter-compatible format

        # Display the image on the canvas
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Add Heading Label
        heading = tk.Label(self, text="Inventory Management System for Pepper", font=("Arial", 36, "bold"),
                           bg="black", fg="white")
        heading.place(relx=0.5, rely=0.1, anchor="center")

        # Create buttons to navigate to other pages and place them over the image
        button1 = tk.Button(self, text="Go to Imports", command=self.show_import_page,
                            bg="#4CAF50", fg="black",
                            relief="raised",
                            padx=10, pady=5)
        button1.place(relx=0.01, rely=0.3, anchor="nw")

        button2 = tk.Button(self, text="Go to Exports", command=self.show_export_page,
                            bg="#2196F3", fg="black",
                            relief="raised",
                            padx=10, pady=5)
        button2.place(relx=0.01, rely=0.4, anchor="nw")

        button3 = tk.Button(self, text="Show Logs", command=self.show_logs_page,
                            bg="#f44336", fg="black",
                            relief="raised",
                            padx=10, pady=5)
        button3.place(relx=0.01, rely=0.5, anchor="nw")

        button4 = tk.Button(self, text="Inventory", command=self.show_inventory,
                            bg="#f44336", fg="black",
                            relief="raised",
                            padx=10, pady=5)
        button4.place(relx=0.01, rely=0.6, anchor="nw")

    def show_import_page(self):
        self.destroy()  # Close the homepage
        ImportPage()    # Open Import Page

    def show_export_page(self):
        self.destroy()  # Close the homepage
        ExportPage()    # Open Export Page

    def show_logs_page(self):
        self.destroy()
        ViewDataPage()

    def change_bgcolor(self, button, color):
        """Function to change button background color on hover."""
        button.config(bg=color)

    def show_inventory(self):
        """Show the current inventory level in kg and warn if nearing capacity."""
        MAX_CAPACITY = 10000  # Maximum storage capacity in kg
        WARNING_THRESHOLD = 0.8  # 80% threshold
        WARNING_LOW = 0.01

        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()

        try:
            # Calculate total imports and exports
            cursor.execute("SELECT SUM(quantity) FROM imports1")
            total_imports = cursor.fetchone()[0] or 0

            cursor.execute("SELECT SUM(quantity) FROM exports1")
            total_exports = cursor.fetchone()[0] or 0

            # Calculate current inventory
            current_inventory = total_imports - total_exports

            # Show warning if inventory exceeds 80% capacity
            if current_inventory >= MAX_CAPACITY:
                messagebox.showerror("Inventory Full",
                                     f"⚠️ Inventory is FULL! Cannot add more stock.\nCurrent Inventory: {current_inventory} kg")
            elif current_inventory >= WARNING_THRESHOLD * MAX_CAPACITY:
                messagebox.showwarning("Inventory Warning",
                                       f"⚠️ Inventory is almost full!\nCurrent Inventory: {current_inventory} kg\nCapacity: {MAX_CAPACITY} kg")
            elif current_inventory <= WARNING_LOW * MAX_CAPACITY:
                messagebox.showwarning("Inventory Warning",
                                       f"⚠️ Inventory is almost empty\nCurrent Inventory: {current_inventory} kg\nCapacity: {MAX_CAPACITY} kg")

            # Show current inventory status
            else:
                messagebox.showinfo("Current Inventory",
                                    f"Current Inventory: {current_inventory} kg\nCapacity: {MAX_CAPACITY} kg")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error fetching inventory data: {e}")

        finally:
            conn.close()


if __name__ == "__main__":
    app = HomePage()
    app.mainloop()