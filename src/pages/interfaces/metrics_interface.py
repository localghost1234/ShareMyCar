# metrics_interface.py
import tkinter as tk
from tkinter import messagebox

from src.pages.interfaces.base_interface import BaseInterface

class MetricsInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root, "Financial Metrics", system)

        self.view_button = tk.Button(self.frame, text="View Metrics", command=self.view_metrics)
        self.view_button.pack()

    def view_metrics(self):
        metrics = self.system.get_metrics()
        metrics_info = f"Total Revenue: €{metrics['total_revenue']}\nTotal Costs: €{metrics['total_costs']}\nTotal Profit: €{metrics['total_profit']}"
        messagebox.showinfo("Financial Metrics", metrics_info)