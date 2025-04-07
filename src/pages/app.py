from src.misc.constants import INTERFACES_CLASS             # Import a list with all the possible interfaces for the user to see (7 in total)
from src.core.system import System                          # Import the System class, which manages the core functionality of the application and its relationship with the database
import signal, sys                                          # Import of libraries for usage of system features

class App:
    """Main application class for Share My Car.

    This class initializes the CLI window, manages the user interface,
    and handles switching between different application interfaces.

    Attributes:
        system (System): The core management module, which takes care of database usage.
        current_interface (BaseInterface): The currently active screen that the user is seeing.
    """

    def __init__(self):
        """Initialize the application.

        Sets up the system (database) and initializes the interface.
        By default, it opens up in 'HomeInterface'
        """
        self.system = System()                                                   # Initialize the core system and database
        self.current_interface = None                                            # Initialize variable to keep track of which interface is displayed
        
        on_close_app = lambda x, y: self.close_app()                             # signal.signal() asks for two params with event info, which aren't really necessary to close the app
        signal.signal(signal.SIGINT, on_close_app)                               # This accounts for closing the app with the 'Ctrl + C' command
        signal.signal(signal.SIGTERM, on_close_app)                              # This accounts for closing the app with the 'X' button on the window
        
        self.switch_interface(0)                                                 # Start application in interface 0 (HomeInterface)

    def switch_interface(self, interface_number):
        """Switch to a new application interface.

        Args:
            interface_class (class): The class object of the visual representation we wish to see.
                Must be a class that implements a Tkinter interface with a 'frame' attribute.
        """
        if interface_number == 7:                                                        # Checks if user input is '7', which indicates shutdown
            self.close_app()                                                             # Executes app-closing module
            return                                                                       # Stops further code execution
    
        if self.current_interface:                                                       # We ensure that the 'current_interface' we access is not a null object (None)
            self.current_interface = None                                                # This closes/erases the current frame (space in the modal) to make space for a new one
        
        if interface_number == 0:                                                        # Checks if interface number indicates 'HomeInterface' value
            self.current_interface = INTERFACES_CLASS[0](self.switch_interface)          # Initiates HomeInterface instance and passes reference to 'current_interface', while passing the reference to this method to allow for screen switching
        else:                                                                                                               # Alternative code to condition
            self.current_interface = INTERFACES_CLASS[interface_number](lambda: self.switch_interface(0), self.system)      # We call the class we wish to see, and pass on information about the app, as well as a Callable to switch back to HomeInterface

    def close_app(self):
        """Handle application shutdown; closes the database the CLI window correctly."""
        del self.system                     # Deletes System instance (which shuts down database gracefully, also)
        print('Shutting down.')             # Shows a closing message on the console
        sys.exit()                          # Closes the window