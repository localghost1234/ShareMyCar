import tkinter as tk
from src.pages.interfaces.base_interface import BaseInterface

# Define column headers
headers = ("ID", "Brand", "Model", "Current Mileage", "Maintenance Cost")
header_row = (
    f"{headers[0]:<5} | "
    f"{headers[1]:<15} | "
    f"{headers[2]:<15} | "
    f"{headers[3]:<15} | "
    f"{headers[4]:<15}"
)
separator_row = "-" * 80

class MaintenanceInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root, system, "Maintenance Management", "Vehicles Needing Maintenance")

        # Create a scrollable Listbox
        self.create_scrollable_listbox()

        # Load vehicles requiring maintenance
        self.load_maintenance_vehicles()

    def load_maintenance_vehicles(self):
        """Fetches and displays vehicles that require maintenance."""
        self.listbox.delete(0, tk.END)  # Clear the listbox

        vehicles = self.system.get_vehicles_requiring_maintenance()  # Fetch vehicles
        
        if vehicles:
            self.listbox.insert(tk.END, header_row)  # Insert headers
            self.listbox.insert(tk.END, separator_row)  # Insert a separator line

            for v in vehicles:
                vehicle_info = (
                    f"{v[0]:<5} | "
                    f"{v[1]:<15} | "
                    f"{v[2]:<15} | "
                    f"{v[3]:<15} | "
                    f"€{v[4]:<14}"
                )
                self.listbox.insert(tk.END, vehicle_info)
        else:
            self.listbox.insert(tk.END, "All vehicles are in good condition.")