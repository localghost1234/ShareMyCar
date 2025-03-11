import tkinter as tk
from src.pages.interfaces.base_interface import BaseInterface

# Define column headers
headers = ("ID", "Brand", "Model", "Current Mileage", "Maintenance Cost")
header_row = " | ".join(f"{h:<10}" for h in headers)

generate_model = lambda content: (
    f"{content[0]:<10} | "
    f"{content[1]:<10} | "
    f"{content[2]:<10} | "
    f"{content[3]:<10} | "
    f"€{content[4]:<10}"
)

class MaintenanceInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root, system, "Maintenance Management", "Vehicles Needing Maintenance")

        # Create a scrollable Listbox
        self.create_scrollable_listbox()

        # Load vehicles requiring maintenance
        self.load_content(
            get_content=self.system.get_vehicles_requiring_maintenance,
            generate_model=generate_model,
            header_row=header_row,
            empty_message="All vehicles are in good condition."
        )