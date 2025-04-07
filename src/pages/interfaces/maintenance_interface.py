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
        super().__init__(*MAINTENANCE.TITLES, system=system)                             # Initializes 'BaseInterface' with the pre-defined TITLES strings

        has_content = self.load_content(                                                          # Loads the list with vehicles that need maintenance
                headers=MAINTENANCE.HEADERS,
                get_content=self.system.get_vehicles_requiring_maintenance,             # Function to fetch vehicles requiring maintenance
                generate_model=MAINTENANCE.GENERATE_MODEL,                              # Formatting function for vehicle data
                empty_message=MAINTENANCE.EMPTY_MESSAGE,                                # Message to display if no vehicles require maintenance
            )

        if has_content:
            action_number = self.input_loop(MAINTENANCE.VALIDATOR, MAINTENANCE.LOOP_MESSAGE)
            if action_number == 1:
                self.check_maintenance()
            
        on_return_home()

    def check_maintenance(self):
        """
        Displays confirmation dialog for completing vehicle maintenance.
        """

        try:
            vehicle_id = int(input("Vehicle ID: "))                       # Label for vehicle ID
            is_updated = self.system.query_update_maintenance_mileage(vehicle_id)

            if is_updated:
                print("Maintenance was done successfully!\n")
            else:
                print("Vehicle not found, please try again.\n")
        except ValueError:
            print('Invalid value, please try again.\n')