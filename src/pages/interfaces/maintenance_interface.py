import tkinter as tk
from src.pages.interfaces.base_interface import BaseInterface
from src.misc.strings import MAINTENANCE

class MaintenanceInterface(BaseInterface):
    """ 
    This class defines the interface for managing vehicle maintenance within the system. 
    It inherits from `BaseInterface` and provides a list of vehicles that require maintenance.
    
    Attributes:
        root (tk.Tk or tk.Toplevel): The main application window.
        system (object): The system instance managing vehicle data.
    """

    def __init__(self, root, system):
        """ 
        Initializes the maintenance interface, displaying a list of vehicles that require service.
        
        Args:
            root (tk.Tk or tk.Toplevel): The main application window.
            system (object): The system instance handling vehicle maintenance data.
        """
        super().__init__(root, system, *MAINTENANCE.TITLES)  # Initialize the base interface with maintenance titles

        self.create_scrollable_listbox(MAINTENANCE.HEADERS)  # Create a scrollable list box for displaying vehicle data

        self.load_content(  # Populate the list with vehicles that need maintenance
            get_content=self.system.get_vehicles_requiring_maintenance,  # Function to fetch vehicles requiring maintenance
            generate_model=MAINTENANCE.GENERATE_MODEL,  # Formatting function for vehicle data
            empty_message=MAINTENANCE.EMPTY_MESSAGE,  # Message to display if no vehicles require maintenance
        )
