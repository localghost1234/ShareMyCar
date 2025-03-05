# logs_interface.py
import tkinter as tk
from tkinter import messagebox

from src.pages.interfaces.base_interface import BaseInterface

class LogsInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root, "Transaction Logs", system)

        self.view_button = tk.Button(self.frame, text="View Logs", command=self.view_logs)
        self.view_button.pack()

    def view_logs(self):
        logs_info = "\n".join([f"Vehicle ID: {log['vehicle_id']}, Cost: €{log['total_cost']}" for log in self.system.transaction_logs])
        messagebox.showinfo("Transaction Logs", logs_info if logs_info else "No logs available.")