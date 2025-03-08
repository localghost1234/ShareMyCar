import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # For better-looking widgets

from src.core.vehicle import Vehicle
from src.pages.interfaces.base_interface import BaseInterface

class InventoryInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root, "Inventory Management", system)

        self.add_button = tk.Button(self.frame, text="Add Vehicle", command=self.add_vehicle)
        self.add_button.pack()

        self.view_button = tk.Button(self.frame, text="View Vehicles", command=self.view_vehicles)
        self.view_button.pack()

    def add_vehicle(self):
        # Create a custom dialog box
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Vehicle")
        dialog.geometry("300x200")

        # Labels and Entry fields
        tk.Label(dialog, text="Brand:").grid(row=0, column=0, padx=10, pady=5)
        brand_entry = tk.Entry(dialog)
        brand_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(dialog, text="Model:").grid(row=1, column=0, padx=10, pady=5)
        model_entry = tk.Entry(dialog)
        model_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(dialog, text="Mileage:").grid(row=2, column=0, padx=10, pady=5)
        mileage_entry = tk.Entry(dialog)
        mileage_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(dialog, text="Daily Price:").grid(row=3, column=0, padx=10, pady=5)
        daily_price_entry = tk.Entry(dialog)
        daily_price_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(dialog, text="Maintenance Cost:").grid(row=4, column=0, padx=10, pady=5)
        maintenance_cost_entry = tk.Entry(dialog)
        maintenance_cost_entry.grid(row=4, column=1, padx=10, pady=5)

        # Submit button
        submit_button = tk.Button(dialog, text="Submit", command=lambda: self.submit_vehicle(
            brand_entry.get(),
            model_entry.get(),
            mileage_entry.get(),
            daily_price_entry.get(),
            maintenance_cost_entry.get(),
            dialog
        ))
        submit_button.grid(row=5, column=0, columnspan=2, pady=10)

    def submit_vehicle(self, brand, model, mileage, daily_price, maintenance_cost, dialog):
        # Validate inputs
        if not brand or not model or not mileage or not daily_price or not maintenance_cost:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            mileage = int(mileage)
            daily_price = float(daily_price)
            maintenance_cost = float(maintenance_cost)
        except ValueError:
            messagebox.showerror("Error", "Invalid input for mileage, daily price, or maintenance cost.")
            return

        # Add the vehicle to the database
        self.system.add_vehicle(brand, model, mileage, daily_price, maintenance_cost)
        messagebox.showinfo("Success", "Vehicle added!")

        # Close the dialog box
        dialog.destroy()

    def view_vehicles(self):
        vehicles = self.system.get_all_vehicles()
        
        if vehicles:
            vehicles_info = "".join([
                f"ID: {v[0]}\n"
                f"Brand: {v[1]}\n"
                f"Model: {v[2]}\n"
                f"Current Mileage: {v[3]} miles\n"
                f"Next Maintenance: {v[4]} miles\n"
                f"Daily Price: €{v[5]}\n"
                f"Maintenance Cost: €{v[6]}/mile\n"
                f"Available: {'Yes' if v[7] else 'No'}\n"
                "\n"
                for v in vehicles
            ])
            messagebox.showinfo("Vehicles", vehicles_info)
        else:
            messagebox.showinfo("Vehicles", "No vehicles available.")
