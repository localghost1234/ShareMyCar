# return_interface.py
import tkinter as tk
from tkinter import messagebox

from src.pages.interfaces.base_interface import BaseInterface

class ReturnInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root, "Return Management", system)

        self.return_button = tk.Button(self.frame, text="Return Vehicle", command=self.return_vehicle)
        self.return_button.pack()

    def return_vehicle(self):
        total_cost = self.system.return_vehicle(1, 120, 2)  # Example: Vehicle ID 1, 120 km, 2 late days
        if total_cost:
            messagebox.showinfo("Success", f"Vehicle returned! Total cost: €{total_cost}")
        else:
            messagebox.showerror("Error", "Vehicle not found.")