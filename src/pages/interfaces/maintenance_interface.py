import tkinter as tk
from src.pages.interfaces.base_interface import BaseInterface

titles = ("Maintenance Management", "Vehicles Needing Maintenance")
headers = ("ID", "Brand", "Model", "Current Mileage", "Maintenance Cost")
header_row = " | ".join(f"{h:<10}" for h in headers)
empty_message = "All vehicles are in good condition."

generate_model = lambda content: (
    f"{content[0]:<10} | "
    f"{content[1]:<10} | "
    f"{content[2]:<10} | "
    f"{content[3]:<10} | "
    f"€{content[4]:<10}"
)

class MaintenanceInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root, system, *titles)

        # Create a scrollable Listbox
        self.create_scrollable_listbox(header_row)

        # Load vehicles requiring maintenance
        self.load_content(
            get_content=self.system.get_vehicles_requiring_maintenance,
            generate_model=generate_model,
            empty_message=empty_message,
        )