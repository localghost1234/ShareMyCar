# metrics_interface.py
import tkinter as tk
from src.pages.interfaces.base_interface import BaseInterface

class MetricsInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root, "Financial Metrics", system)
        
        tk.Label(self.frame, text="Financial Metrics:").pack()

        # Frame for financial data
        self.metrics_frame = tk.Frame(self.frame)
        self.metrics_frame.pack(fill=tk.BOTH, expand=True)

        # Text widget to display financial data
        self.metrics_text = tk.Text(
            self.metrics_frame, height=10, width=80, wrap="none"
        )
        self.metrics_text.pack(fill=tk.BOTH, expand=True)

        # Load financial data
        self.load_metrics()
    
    def load_metrics(self):
        """Fetches and displays financial metrics."""
        self.metrics_text.config(state=tk.NORMAL)
        self.metrics_text.delete("1.0", tk.END)

        metrics = self.system.get_financial_metrics()
        
        if metrics:
            headers = ["Total Revenue (€)", "Total Costs (€)", "Total Profit (€)", "Avg Mileage (km/vehicle)"]
            header_row = (
                f"{headers[0]:<20} | "
                f"{headers[1]:<20} | "
                f"{headers[2]:<20} | "
                f"{headers[3]:<20}"
            )
            self.metrics_text.insert(tk.END, header_row + "\n")
            self.metrics_text.insert(tk.END, "-" * 90 + "\n")

            metrics_row = (
                f"{metrics['total_revenue']:<20.2f} | "
                f"{metrics['total_costs']:<20.2f} | "
                f"{metrics['total_profit']:<20.2f} | "
                f"{metrics['average_mileage']:<20.2f}"
            )
            self.metrics_text.insert(tk.END, metrics_row + "\n")
        else:
            self.metrics_text.insert(tk.END, "No financial data available.")

        self.metrics_text.config(state=tk.DISABLED)