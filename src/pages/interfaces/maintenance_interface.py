import tkinter as tk
from src.pages.interfaces.base_interface import BaseInterface

class MaintenanceInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root, "Maintenance Management", system)
        
        tk.Label(self.frame, text="Vehicles Needing Maintenance:").pack()

        # Frame for vehicle list with scrollbars
        self.vehicle_frame = tk.Frame(self.frame)
        self.vehicle_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbars (vertical and horizontal)
        self.v_scrollbar = tk.Scrollbar(self.vehicle_frame, orient=tk.VERTICAL)
        self.h_scrollbar = tk.Scrollbar(self.vehicle_frame, orient=tk.HORIZONTAL)

        # Text widget with both scrollbars
        self.maintenance_text = tk.Text(
            self.vehicle_frame, height=15, width=70, wrap="none",
            yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set
        )
        
        # Pack elements properly
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.maintenance_text.pack(fill=tk.BOTH, expand=True)

        # Link scrollbars
        self.v_scrollbar.config(command=self.maintenance_text.yview)
        self.h_scrollbar.config(command=self.maintenance_text.xview)

        self.load_maintenance_vehicles()

    def load_maintenance_vehicles(self):
        """Fetches and displays vehicles that require maintenance."""
        self.maintenance_text.config(state=tk.NORMAL)
        self.maintenance_text.delete("1.0", tk.END)

        vehicles = self.system.get_vehicles_requiring_maintenance()

        if vehicles:
            for v in vehicles:
                vehicle_info = (
                    f"ID: {v[0]}\t"
                    f"Brand: {v[1]}\t"
                    f"Model: {v[2]}\t"
                    f"Current Mileage: {v[3]} kms\t"
                    f"Next Maintenance: {v[4]} kms\t"
                    f"Maintenance Cost: €{v[5]}/km\n"
                )
                self.maintenance_text.insert(tk.END, vehicle_info)
        else:
            self.maintenance_text.insert(tk.END, "All vehicles are in good condition.")

        self.maintenance_text.config(state=tk.DISABLED)

