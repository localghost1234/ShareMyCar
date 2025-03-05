# inventory_interface.py
import tkinter as tk
from tkinter import messagebox, simpledialog

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
        # Get vehicle details from the user
        brand = simpledialog.askstring("Input", "Enter brand:")
        model = simpledialog.askstring("Input", "Enter model:")
        mileage = simpledialog.askinteger("Input", "Enter mileage:")
        daily_price = simpledialog.askfloat("Input", "Enter daily price:")
        maintenance_cost = simpledialog.askfloat("Input", "Enter maintenance cost per km:")

        if brand and model and mileage is not None and daily_price is not None and maintenance_cost is not None:
            # Add the vehicle to the database
            self.system.add_vehicle(brand, model, mileage, daily_price, maintenance_cost)
            messagebox.showinfo("Success", "Vehicle added!")
        else:
            messagebox.showerror("Error", "All fields are required.")

    def view_vehicles(self):
        vehicles = self.system.get_vehicles()
        if vehicles:
            vehicles_info = "\n".join([
                f"ID: {v[0]}, Brand: {v[1]}, Model: {v[2]}, Mileage: {v[3]} km, "
                f"Daily Price: €{v[4]}, Maintenance Cost: €{v[5]}/km, "
                f"Available: {'Yes' if v[6] else 'No'}"
                for v in vehicles
            ])
            messagebox.showinfo("Vehicles", vehicles_info)
        else:
            messagebox.showinfo("Vehicles", "No vehicles available.")