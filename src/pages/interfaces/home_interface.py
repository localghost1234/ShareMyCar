import sys
from src.pages.interfaces.base_interface import BaseInterface
from src.misc.constants import INTERFACES_LIST

class HomeInterface(BaseInterface):
    """
        A class with a simple visual representation for welcoming the user.
        Only used on application's startup.
    """
    def __init__(self, system):
        super().__init__(system, "SHARE MY CAR") # We initialize parent class (BaseInterface) to make it look similar to other interfaces

        # Displays simple strings of messages, with varying types of letter and sizes
        print("Welcome to the car sharing management system!")

        interface_number = 0
        
        while interface_number < 1 and interface_number > 7:
            print("Please select a valid operation (1-7):\n")
            interface_number = input(
                "1) Vehicle Inventory\n"
                "2) Book Vehicle\n"
                "3) Return Vehicle\n"
                "4) Vehicle Maintenance\n"
                "5) Check Logs\n"
                "6) Financial Metrics\n"
                "7) Exit\n\n"
            )

        if interface_number == 7:
            self.on_close()
            return

        new_interface = INTERFACES_LIST[interface_number + 1]
        self.switch_interface(new_interface)
        
    def switch_interface(self, interface_class):
        """Switch to a new application interface.

        Args:
            interface_class (class): The class object of the visual representation we wish to see.
                Must be a class that implements a Tkinter interface with a 'frame' attribute.
        """
        if self.current_interface:                                              # We ensure that the 'current_interface' we access is not a null object (None)
            self.current_interface = None                                       # This closes/erases the current frame (space in the modal) to make space for a new one
        self.current_interface = interface_class(self.system)                              # We call the class we wish to see, and pass on information about the app


    def on_close(self):
        """
        Handle application shutdown.
        
        Closes the system and destroys the Tkinter root window.
        Executed when the user clicks the window's close button.
        """
        print('Shutting down.')             # Shows a closing message on the delevoper's console
        self.system.close()                 # Direct command with database to shut it down carefully
        sys.exit()                          # Erases the main Frame/modal with the whole app