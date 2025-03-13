import tkinter as tk
from src.pages.interfaces.base_interface import BaseInterface

class HomeInterface(BaseInterface):
    def __init__(self, root, system):
        super().__init__(root,  system, "SHARE MY CAR")

        tk.Label(self.frame, text="Welcome to the car sharing management system!", font=("Helvetica", 15, "bold")).pack(pady=20)
        tk.Label(self.frame, text="Please select any operation you wish to perform", font=("Helvetica", 14)).pack()