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

        tk.Button(self.frame, text="Query Metric", command=self.query_metric).pack(pady=20)
        tk.Button(self.frame, text="Download Full Report", command=self.generate_full_report).pack(pady=2)

    def query_metric(self):
        pass

    def generate_full_report(self):
        pass
