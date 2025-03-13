# app.py
import tkinter as tk

from src.core.system import System
from src.pages.interfaces.home_interface import HomeInterface
from src.misc.constants import INTERFACES_LIST

class App:
    def __init__(self):
        self.system = System()
        self.current_interface = None

        self.root = tk.Tk()
        self.root.geometry("720x480")
        self.root.title("Share My Car")

        button_frame = tk.Frame(self.root)
        button_frame.pack()

        for interface_name, interface_class in INTERFACES_LIST:
            button = tk.Button(button_frame, text=interface_name, command=lambda i=interface_class: self.switch_interface(i))
            button.pack(side=tk.LEFT)

        # Start with the HomeInterface
        self.switch_interface(HomeInterface)

        # Register on_close() as the handler for the window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.root.mainloop()

    def switch_interface(self, interface_class):
        if self.current_interface:
            self.current_interface.frame.destroy()

        self.current_interface = interface_class(self.root, self.system)

    def on_close(self):
        print('Shutting down.')
        
        self.system.close()
        self.root.destroy()