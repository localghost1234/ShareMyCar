from src.pages.interfaces.base_interface import BaseInterface       # Import the BaseInterface class, a parent class providing common functionality for other interfaces
from src.misc.strings import LOGS                                   # Import the LOGS namespace, containing strings or configurations for the logs interface

class LogsInterface(BaseInterface):
    """ 
    Interface for displaying transaction logs within the system.
    
    This class extends `BaseInterface` and presents a structured list of recorded transactions.
    It initializes a scrollable listbox and loads log entries retrieved from the system.

    Attributes:
        system: Reference to the application's System instance
        frame: The main container frame for the interface
    """

    def __init__(self, root, system):
        """Initialize the logs interface with log entries display.
        
        Args:
            root (tk.Tk): The root window
            system: Reference to the application's System instance
        """
        super().__init__(root, system, *LOGS.TITLES)            # Initializes 'BaseInterface' with the pre-defined TITLES strings

        self.create_scrollable_listbox(LOGS.HEADERS)            # Create a scrollable listbox for log entries

        self.load_content(                                      # Load transaction logs into the Listbox components
            get_content=self.system.get_all_logs,               # Function to fetch log data from database
            generate_model=LOGS.GENERATE_MODEL,                 # Formatting model for displaying logs
            empty_message=LOGS.EMPTY_MESSAGE,                   # Message shown if no logs are available
        )