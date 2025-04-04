from src.pages.interfaces.base_interface import BaseInterface       # Import the BaseInterface class, a parent class providing common functionality for other interfaces
from src.misc.interface_strings import MAINTENANCE                            # Import the MAINTENANCE namespace, containing strings or configurations for the maintenance interface
from src.misc.utilities import input_loop

class MaintenanceInterface(BaseInterface):
    """ 
    Interface for managing vehicle maintenance.
    
    Displays vehicles requiring maintenance and allows:
    - Viewing maintenance-required vehicles
    - Updating maintenance status
    - Resetting maintenance mileage
    
    Inherits from BaseInterface for common functionality.
    
    Attributes:
        refresh_listbox (function): Callback to refresh the vehicle list
    """

    def __init__(self, on_return_home, system):
        """Initialize the maintenance interface with vehicle list and event bindings.
        
        Args:
            system: Reference to the application's System instance
        """
        super().__init__(system, *MAINTENANCE.TITLES)                             # Initializes 'BaseInterface' with the pre-defined TITLES strings

        self.refresh_listbox = lambda: (                                                # Creates an executable function to be used around interface
            self.load_content(                                                          # Loads the list with vehicles that need maintenance
                headers=MAINTENANCE.HEADERS,
                get_content=self.system.get_vehicles_requiring_maintenance,             # Function to fetch vehicles requiring maintenance
                generate_model=MAINTENANCE.GENERATE_MODEL,                              # Formatting function for vehicle data
                empty_message=MAINTENANCE.EMPTY_MESSAGE,                                # Message to display if no vehicles require maintenance
            )
        )

        self.refresh_listbox()                                                          # Loads content using locally created callback

        is_valid = lambda num: num < 1 or num > 2
        message = """Choose an action:
                        1) Remove vehicle from list
                        2) Return to main menu
                        
                        """
        
        action_number = input_loop(is_valid, message)

        if action_number == 1:
            self.check_maintenance()
            
        on_return_home()

    def check_maintenance(self):
        """
        Displays confirmation dialog for completing vehicle maintenance.
        """

        vehicle_id = input("Vehicle ID: ")                       # Label for vehicle ID
        
        self.system.query_update_maintenance_mileage(vehicle_id)
        self.refresh_listbox()