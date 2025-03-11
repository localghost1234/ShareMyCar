import tkinter as tk
from src.pages.interfaces.base_interface import BaseInterface

titles = ("Metrics Management", "Financial Metrics")
headers = ("Total Revenue (€)", "Total Costs (€)", "Total Profit (€)", "Avg Mileage (km/vehicle)")
header_row = " | ".join(f"{h:<20}" for h in headers)
empty_message = "No financial data available."

generate_model = lambda content: (
    f"{content[0]:<20} | "
    f"{content[1]:<20} | "
    f"{content[2]:<20} | "
    f"{content[3]:<20}"
)

class MetricsInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root, system, *titles)

        # Create a scrollable Listbox
        self.create_scrollable_listbox(header_row)

        # Load financial metrics
        self.load_content(
            get_content=self.system.get_financial_metrics,
            generate_model=generate_model,
            empty_message=empty_message,
        )