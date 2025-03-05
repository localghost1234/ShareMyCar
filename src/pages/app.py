# main.py
import tkinter as tk

from src.core.system import CarsharingSystem
from src.pages.interfaces.inventory_interface import InventoryInterface
from src.pages.interfaces.logs_interface import LogsInterface
from src.pages.interfaces.maintenance_interface import MaintenanceInterface
from src.pages.interfaces.metrics_interface import MetricsInterface
from src.pages.interfaces.return_interface import ReturnInterface
from src.pages.interfaces.scheduling_interface import SchedulingInterface

class App:
    def __init__(self, root):
        self.root = root
        self.system = CarsharingSystem()
        self.current_interface = None

        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        interfaces = [
            ("Inventory", InventoryInterface),
            ("Scheduling", SchedulingInterface),
            ("Return", ReturnInterface),
            ("Maintenance", MaintenanceInterface),
            ("Logs", LogsInterface),
            ("Metrics", MetricsInterface),
        ]

        for interface_name, interface_class in interfaces:
            button = tk.Button(self.button_frame, text=interface_name, command=lambda i=interface_class: self.switch_interface(i))
            button.pack(side=tk.LEFT)

        # Start with the Inventory interface
        self.switch_interface(InventoryInterface)

    def switch_interface(self, interface_class):
        if self.current_interface:
            self.current_interface.frame.destroy()

        self.current_interface = interface_class(self.root, self.system)

    def on_close(self):
        # Close the database connection
        self.system.close()
        self.root.destroy()