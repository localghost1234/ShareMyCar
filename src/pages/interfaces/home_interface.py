import tkinter as tk
from src.pages.interfaces.base_interface import BaseInterface

class HomeInterface(BaseInterface):
    """
        A class with a simple visual representation for welcoming the user.
        Only used on application's startup.
    """
    def __init__(self, root, system):
        super().__init__(root,  system, "SHARE MY CAR") # We initialize parent class (BaseInterface) to make it look similar to other interfaces

        # Displays simple strings of messages, with varying types of letter and sizes
        tk.Label(self.frame, text="Welcome to the car sharing management system!", font=("Helvetica", 15, "bold")).pack(pady=50)
        tk.Label(self.frame, text="Please select any operation you wish to perform", font=("Helvetica", 14)).pack(pady=10)