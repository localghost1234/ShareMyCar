from src.pages.interfaces.base_interface import BaseInterface       # Import the BaseInterface class, a parent class providing common functionality for other interfaces
from src.misc.interface_strings import MAINTENANCE                            # Import the MAINTENANCE namespace, containing strings or configurations for the maintenance interface

class MaintenanceInterface(BaseInterface):
    """ 
    Interface for managing vehicle maintenance.
    
    Displays vehicles requiring maintenance and allows:
    - Viewing maintenance-required vehicles
    - Updating maintenance status
    - Resetting maintenance mileage
    """

    def __init__(self, on_return_home, system):
        """Initialize the maintenance interface with vehicle list and event bindings.
        
        Args:
            on_return_home (Callable): Function used to go back to main menu interface
            system (System): Reference to the application's System instance
        """
        super().__init__(*MAINTENANCE.TITLES, system=system)                            # Initializes 'BaseInterface' with the pre-defined TITLES strings

        has_content = self.load_content(                                                # Loads the list with vehicles that need maintenance
                headers=MAINTENANCE.HEADERS,                                            # Set of strings that will be displayed at the very top (column names)
                get_content=self.system.get_vehicles_requiring_maintenance,             # Function to fetch vehicles requiring maintenance
                generate_model=MAINTENANCE.GENERATE_MODEL,                              # Formatting function for vehicle data
                empty_message=MAINTENANCE.EMPTY_MESSAGE,                                # Message to display if no vehicles require maintenance
            )

        if has_content:                                                                         # Checks if content was found
            action_number = self.input_loop(MAINTENANCE.VALIDATOR, MAINTENANCE.LOOP_MESSAGE)    # Activates loop with validating callable and message to display, then assigns the (cleaned) user input
            if action_number == 1:                                                              # Checks if allowed action was chosen
                self.check_maintenance()                                                        # Executes function if condition was met
            
        on_return_home()                                                                        # Returns to main menu

    def check_maintenance(self):
        """Displays section to complete vehicle maintenance."""
        try:                                                                            # Creates scope to handle any errors
            vehicle_id = abs(int(input("Vehicle ID: ")))                                # Obtains vehicle_id from user input, which is checked to be a positive integer
            is_updated = self.system.query_update_maintenance_mileage(vehicle_id)       # Updates database to new maintenance mileage, and returns boolean
            if is_updated:                                                              # Checks if vehicle was found and its data updated
                print("Maintenance was done successfully!")                             # Prints a success message
            else:                                                                       # Alternative if vehicle was not found
                print("Vehicle not found, please try again.")                           # Prints error message
        except ValueError:                                                              # If any error is caught, code skips to this line
            print('Invalid value, please try again.')                                   # Prints error message

        print()                                                                         # Prints line break