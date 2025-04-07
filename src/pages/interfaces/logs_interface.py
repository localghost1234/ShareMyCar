from src.pages.interfaces.base_interface import BaseInterface       # Import the BaseInterface class, a parent class providing common functionality for other interfaces
from src.misc.interface_strings import LOGS                                   # Import the LOGS namespace, containing strings or configurations for the logs interface

class LogsInterface(BaseInterface):
    """ 
    Interface for displaying transaction logs within the system.
    """

    def __init__(self, on_return_home, system):
        """Initialize the logs interface with log entries display.
        
        Args:
            on_return_home (Callable): Function used to go back to main menu interface
            system (System): Reference to the application's System instance
        """
        super().__init__(*LOGS.TITLES, system=system)           # Initializes 'BaseInterface' with the pre-defined TITLES strings

        self.load_content(                                      # Load transaction logs into the Listbox components
            headers=LOGS.HEADERS,                               # Set of strings that will be displayed at the very top (column names)
            get_content=self.system.logs,                       # Function to fetch log data from database
            generate_model=LOGS.GENERATE_MODEL,                 # Formatting model for displaying logs
            empty_message=LOGS.EMPTY_MESSAGE,                   # Message shown if no logs are available
        )

        on_return_home()                                        # When the data finishes displaying, returns to main menu automatically