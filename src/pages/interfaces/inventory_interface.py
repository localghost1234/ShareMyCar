# inventory_interface.py
import tkinter as tk
from tkinter import messagebox

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
        vehicle = Vehicle(1, "Toyota", "Corolla", 10000, 50, 0.1)
        self.system.add_vehicle(vehicle)
        messagebox.showinfo("Success", "Vehicle added!")

    def view_vehicles(self):
        vehicles_info = "\n".join([f"{v.brand} {v.model} (ID: {v.id})" for v in self.system.vehicles])
        messagebox.showinfo("Vehicles", vehicles_info if vehicles_info else "No vehicles available.")