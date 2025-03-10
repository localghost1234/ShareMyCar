import tkinter as tk
from src.pages.interfaces.base_interface import BaseInterface

class MetricsInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root, "Financial Metrics", system)
        
        tk.Label(self.frame, text="Financial Metrics:").pack()

        # Create a scrollable Listbox
        self.metrics_listbox = self.create_scrollable_listbox()

        # Load financial metrics
        self.load_metrics()

    def load_metrics(self):
        """Fetches and displays financial metrics."""
        self.metrics_listbox.delete(0, tk.END)  # Clear the listbox

        metrics = self.system.get_financial_metrics()  # Fetch metrics
        
        if metrics:
            # Define column headers
            headers = ["Total Revenue (€)", "Total Costs (€)", "Total Profit (€)", "Avg Mileage (km/vehicle)"]
            header_row = (
                f"{headers[0]:<20} | "
                f"{headers[1]:<20} | "
                f"{headers[2]:<20} | "
                f"{headers[3]:<20}"
            )
            self.metrics_listbox.insert(tk.END, header_row)  # Insert headers
            self.metrics_listbox.insert(tk.END, "-" * 90)  # Insert a separator line

            # Insert metrics data
            metrics_row = (
                f"{metrics['total_revenue']:<20.2f} | "
                f"{metrics['total_costs']:<20.2f} | "
                f"{metrics['total_profit']:<20.2f} | "
                f"{metrics['average_mileage']:<20.2f}"
            )
            self.metrics_listbox.insert(tk.END, metrics_row)
        else:
            self.metrics_listbox.insert(tk.END, "No financial data available.")