# scheduling_interface.py
import tkinter as tk
from tkinter import messagebox

from src.pages.interfaces.base_interface import BaseInterface

class SchedulingInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root, "Scheduling Management", system)

        self.book_button = tk.Button(self.frame, text="Book Vehicle", command=self.book_vehicle)
        self.book_button.pack()

    def book_vehicle(self):
        cost = self.system.book_vehicle(1, 3, 100)  # Example: Vehicle ID 1, 3 days, 100 km
        if cost:
            messagebox.showinfo("Success", f"Vehicle booked! Estimated cost: €{cost}")
        else:
            messagebox.showerror("Error", "Vehicle not found.")