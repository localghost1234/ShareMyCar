from src.pages.interfaces.base_interface import BaseInterface       # Import the BaseInterface class, which serves as a parent class for other interfaces
from src.misc.interface_strings import HOME

class HomeInterface(BaseInterface):
    """
        A class with a simple visual representation for welcoming the user.
        Only used on application's startup.
    """
    def __init__(self, on_switch_interface):
        super().__init__(HOME.TITLE)
        action_number = self.input_loop(HOME.VALIDATOR, HOME.LOOP_MESSAGE)
        print()
        on_switch_interface(action_number)

