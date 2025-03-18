from src.pages.interfaces.base_interface import BaseInterface       # Import the BaseInterface class, a parent class providing common functionality for other interfaces
from src.misc.strings import MAINTENANCE                            # Import the MAINTENANCE constant, containing strings or configurations for the maintenance interface

class MaintenanceInterface(BaseInterface):
    """ 
        This class defines the interface for showcasing vehicles in need of maintenance.
        Iinherits from components from `BaseInterface`.
    """

    def __init__(self, root, system):
        super().__init__(root, system, *MAINTENANCE.TITLES)                 # Initializes 'BaseInterface' with the pre-defined TITLES strings

        self.create_scrollable_listbox(MAINTENANCE.HEADERS)                 # Sets a Listbox component with the column names of the displayed info

        self.load_content(                                                  # Loads the list with vehicles that need maintenance
            get_content=self.system.get_vehicles_requiring_maintenance,     # Function to fetch vehicles requiring maintenance
            generate_model=MAINTENANCE.GENERATE_MODEL,                      # Formatting function for vehicle data
            empty_message=MAINTENANCE.EMPTY_MESSAGE,                        # Message to display if no vehicles require maintenance
        )
