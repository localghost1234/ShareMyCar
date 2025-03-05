# maintenance_interface.py
import tkinter as tk
from tkinter import messagebox

from src.pages.interfaces.base_interface import BaseInterface

class MaintenanceInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root, "Maintenance Management", system)

        self.maintenance_button = tk.Button(self.frame, text="Schedule Maintenance", command=self.schedule_maintenance)
        self.maintenance_button.pack()

    def schedule_maintenance(self):
        messagebox.showinfo("Info", "Maintenance scheduled for all vehicles over 10,000 km.")