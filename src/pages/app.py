from src.core.system import System                                          # Import the System class, which manages the core functionality of the application and its relationship with the database
from src.pages.interfaces.home_interface import HomeInterface               # Import the HomeInterface class, representing the home page (welcoming interface)
import signal

class App:
    """Main application class for Share My Car.

    This class initializes the Tkinter root window, manages the user interface,
    and handles switching between different application interfaces.

    Attributes:
        system (System): The core system managing application functionality.
        current_interface: The currently active interface.
        root (tk.Tk): The main application window.
    """

    def __init__(self):
        """Initialize the application.

        Sets up the system, creates the main window, and initializes the interface.
        By default, it opens up on a one-time usage of 'HomeInterface'

        Initializes:
            - system: Core database administration
            - HomeInterface: Tracks current active interface
        """
        self.system = System()                                                          # Initialize the core system and database
        signal.signal(signal.SIGTERM, self.on_close)                                    # This adds behaviour to the 'X' button on the window
        HomeInterface(self.system)