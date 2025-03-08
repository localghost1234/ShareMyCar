import tkinter as tk
from tkinter import messagebox
from src.pages.interfaces.base_interface import BaseInterface

class MaintenanceInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root, "Maintenance Management", system)
        
        self.label = tk.Label(self.frame, text="Vehicles Needing Maintenance:")
        self.label.pack()
        
        self.maintenance_listbox = tk.Listbox(self.frame, width=50, height=10)
        self.maintenance_listbox.pack()
        
        self.load_maintenance_vehicles()

    def load_maintenance_vehicles(self):
        vehicles = self.system.get_vehicles_requiring_maintenance()
        
        if vehicles:
            for v in vehicles:
                self.maintenance_listbox.insert(tk.END, f"ID: {v[0]}, {v[1]} {v[2]} - {v[3]} miles")
        else:
            self.maintenance_listbox.insert(tk.END, "All vehicles are in good condition")
