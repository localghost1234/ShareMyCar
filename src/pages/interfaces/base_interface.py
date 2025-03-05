# base_interface.py
import tkinter as tk

class BaseInterface:
    def __init__(self, root, title, system):
        self.root = root
        self.system = system
        self.frame = tk.Frame(root)
        self.frame.pack()

        self.title_label = tk.Label(self.frame, text=title, font=("Arial", 16))
        self.title_label.pack(pady=10)