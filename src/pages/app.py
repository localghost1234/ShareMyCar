import tkinter as tk
from src.core.system import System
from src.pages.interfaces.home_interface import HomeInterface
from src.misc.constants import INTERFACES_LIST

class App:
    """Main application class for Share My Car.

    This class initializes the Tkinter root window, manages the user interface,
    and handles switching between different application interfaces.
    """

    def __init__(self):
        """Initialize the application.

        Sets up the system, creates the main window, and initializes the interface.
        """
        self.system = System()  # Initialize the core system
        self.current_interface = None  # Track the currently active interface

        self.root = tk.Tk()  # Create the main application window
        self.root.geometry("720x480")  # Set window dimensions
        self.root.title("Share My Car")  # Set window title
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Register on_close to handle window close events

        button_frame = tk.Frame(self.root)  # Create a frame for navigation buttons
        button_frame.pack()

        for interface_name, interface_class in INTERFACES_LIST:  # Create buttons for each interface
            tk.Button(button_frame, text=interface_name, command=lambda i=interface_class: self.switch_interface(i)).pack(side=tk.LEFT)

        self.switch_interface(HomeInterface)  # Start with the HomeInterface
        self.root.mainloop()  # Start the Tkinter event loop

    def switch_interface(self, interface_class):
        """Switch to a new application interface.

        Args:
            interface_class: The class of the interface to switch to.
        """
        if self.current_interface:
            self.current_interface.frame.destroy()  # Destroy the current interface
        self.current_interface = interface_class(self.root, self.system)  # Initialize the new interface

    def on_close(self):
        """Handle application shutdown.

        Closes the system and destroys the Tkinter root window.
        """
        print('Shutting down.')
        self.system.close()  # Close the system
        self.root.destroy()  # Destroy the main window