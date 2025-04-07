from src.misc.constants import INTERFACES_CLASS
from src.core.system import System                                          # Import the System class, which manages the core functionality of the application and its relationship with the database
import signal, sys

class App:
    """Main application class for Share My Car.

    This class initializes the Tkinter root window, manages the user interface,
    and handles switching between different application interfaces.

    Attributes:
        system (System): The core system managing application functionality.
        current_interface: The currently active interface.
    """

    def __init__(self):
        """Initialize the application.

        Sets up the system (database) and initializes the interface.
        By default, it opens up in 'HomeInterface'
        """
        self.system = System()                                                          # Initialize the core system and database
        self.current_interface = None
        
        on_close_app = lambda x, y: self.close_app()                                  # signal.signal() asks for two params with event info, which aren't really necessary to close the app
        signal.signal(signal.SIGINT, on_close_app)                                    # This accounts for closing the app with the 'Ctrl + C' command
        signal.signal(signal.SIGTERM, on_close_app)                                   # This accounts for closing the app with the 'X' button on the window
        self.switch_interface(0)

    def switch_interface(self, interface_number):
        """Switch to a new application interface.

        Args:
            interface_class (class): The class object of the visual representation we wish to see.
                Must be a class that implements a Tkinter interface with a 'frame' attribute.
        """
        if interface_number == 7:
            self.close_app()
            return
    
        if self.current_interface:                                                                                  # We ensure that the 'current_interface' we access is not a null object (None)
            self.current_interface = None                                                                           # This closes/erases the current frame (space in the modal) to make space for a new one
        
        if interface_number == 0:
            self.current_interface = INTERFACES_CLASS[0](self.switch_interface)
        else:
            self.current_interface = INTERFACES_CLASS[interface_number](lambda: self.switch_interface(0), self.system)             # We call the class we wish to see, and pass on information about the app

    def close_app(self):
        """Handle application shutdown.
        
        Closes the database correctly and closes the CLI window.
        """
        del self.system                # Direct command with database to shut it down carefully
        print('Shutting down.')             # Shows a closing message on the delevoper's console
        sys.exit()                          # Closes the window