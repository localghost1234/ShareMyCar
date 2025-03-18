import tkinter as tk
from src.pages.interfaces.base_interface import BaseInterface
from src.misc.strings import LOGS

class LogsInterface(BaseInterface):
    """ 
    Interface for displaying transaction logs within the system.
    
    This class extends `BaseInterface` and presents a structured list of recorded transactions.
    It initializes a scrollable listbox and loads log entries retrieved from the system.
    
    Attributes:
        root (tk.Tk or tk.Toplevel): The main application window where this interface is displayed.
        system (object): The system instance handling transaction logs and operations.
    """

    def __init__(self, root, system):
        """ 
        Initializes the LogsInterface and sets up its components.

        Args:
            root (tk.Tk or tk.Toplevel): The main application window.
            system (object): The system instance managing transaction logs.
        """
        super().__init__(root, system, *LOGS.TITLES)            # Initializes 'BaseInterface' with the pre-defined TITLES strings

        self.create_scrollable_listbox(LOGS.HEADERS)            # Create a scrollable listbox for log entries

        self.load_content(                                      # Load transaction logs into the Listbox components
            get_content=self.system.get_all_transaction_logs,   # Function to fetch log data from database
            generate_model=LOGS.GENERATE_MODEL,                 # Formatting model for displaying logs
            empty_message=LOGS.EMPTY_MESSAGE,                   # Message shown if no logs are available
        )
