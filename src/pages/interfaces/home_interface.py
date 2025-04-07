from src.pages.interfaces.base_interface import BaseInterface       # Import the BaseInterface class, which serves as a parent class for other interfaces
from src.misc.interface_strings import HOME                         # Import the HOME namespace, which contains strings related to the home interface

class HomeInterface(BaseInterface):
    """
        A visual representation to welcome the user and give them instructions.
    """
    def __init__(self, on_switch_interface):
        """Initializes main menu and shows the different actions that can be carried out by the user: switching to another interface, or closing the app.
        
        Args:
            on_switch_interface (Callable): Function which accepts values from numbers 1 to 7, symbolizing the six interfaces and the exit option.
        """
        super().__init__(HOME.TITLE)                                            # Initializes the BaseInterface module with a title string
        action_number = self.input_loop(HOME.VALIDATOR, HOME.LOOP_MESSAGE)      # Puts user into the input loop and obtains their interface choice
        on_switch_interface(action_number)                                      # Allows user to delete this interface instance and go to one of their preference

