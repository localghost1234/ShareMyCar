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
        By default, it opens up on a one-time usage of 'HomeInterface'
        """
        self.system = System()                                                          # Initialize the core system and database
        self.current_interface = None                                                   # Track the currently active interface

        self.root = tk.Tk()                                                             # Create the main application window
        self.root.geometry("720x480")                                                   # Set window dimensions
        self.root.title("Share My Car")                                                 # Set window title
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)                           # This adds behaviour to the 'X' button on the window

        button_frame = tk.Frame(self.root)                                              # Another frame is created on top of the root window, this helps us change interfaces without starting over
        button_frame.pack()                                                             # The .pack() function helps to organize the order of appearance inside a Frame object

        for interface_name, interface_class in INTERFACES_LIST:                                                                             # Iterates over a list with interface information (string with name and python class)
            tk.Button(button_frame, text=interface_name, command=lambda i=interface_class: self.switch_interface(i)).pack(side=tk.LEFT)     # Assigns interface information to a Tkinter Button component and positions it to the leftmost side of the Frame

        self.switch_interface(HomeInterface)                                            # We direct the user to the HomeInterface (only once)
        self.root.mainloop()                                                            # Starts the lifecycle of tkinter, which keeps it running and responsive

    def switch_interface(self, interface_class):
        """Switch to a new application interface.

        Args:
            interface_class: The class object of the visual representation we wish to see.
        """
        if self.current_interface:                                              # We ensure that the 'current_interface' we access is not a null object (None)
            self.current_interface.frame.destroy()                              # This closes/erases the current frame (space in the modal) to make space for a new one
        self.current_interface = interface_class(self.root, self.system)        # We call the class we wish to see, and pass on information about the app

    def on_close(self):
        """
            Handle application shutdown.
            Closes the system and destroys the Tkinter root window.
        """
        print('Shutting down.')             # Shows a closing message on the delevoper's console
        self.system.close()                 # Direct command with database to shut it down carefully
        self.root.destroy()                 # Erases the main Frame/modal with the whole app