import tkinter as tk
from src.pages.interfaces.base_interface import BaseInterface

titles = ("Metrics Management", "Financial Metrics")
headers = ("Total Revenue (€)", "Total Costs (€)", "Total Profit (€)", "Avg Mileage (km/vehicle)")
empty_message = "No financial data available."

class MetricsInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root, system, *titles)

        metrics = self.system.get_financial_metrics()


        tk.Label(self.frame, text="Total Revenue (€):", font=("Arial", 10, "bold")).pack(pady=5)
        tk.Label(self.frame, text=metrics[0], font=("Arial", 8, "italic")).pack()

        tk.Label(self.frame, text="Total Operational Costs (€):", font=("Arial", 10, "bold")).pack(pady=5)
        tk.Label(self.frame, text=metrics[1], font=("Arial", 8, "italic")).pack()

        tk.Label(self.frame, text="Total Profit (€):", font=("Arial", 10, "bold")).pack(pady=5)
        tk.Label(self.frame, text=metrics[2], font=("Arial", 8, "italic")).pack()

        tk.Label(self.frame, text="Average Mileage Per Vehicle (km):", font=("Arial", 10, "bold")).pack(pady=5)
        tk.Label(self.frame, text=metrics[3], font=("Arial", 8, "italic")).pack()

        self.query_metric_button = tk.Button(self.frame, text="Query Metric").pack(pady=20)

        self.download_button = tk.Button(self.frame, text="Download Full Report").pack(pady=2)

    def create_booking(self):
        """Handles booking process by taking input values and calling system logic."""
        try:
            vehicle_id = int(self.vehicle_id_entry.get())
            rental_days = int(self.rental_days_entry.get())
            estimated_km = int(self.estimated_km_entry.get())
            customer_name = str(self.customer_name_entry.get())

            cost = self.system.query_booking(vehicle_id, rental_days, estimated_km, customer_name)
            
            if cost:
                self.show_info(f"Vehicle booked! Estimated cost: €{cost}")
            else:
                self.show_error("Vehicle not found or unavailable.")
        except ValueError:
            self.show_error("Please enter valid numeric values.")
