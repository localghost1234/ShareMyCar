from src.pages.interfaces.base_interface import BaseInterface   # Import the BaseInterface class, a parent class providing common functionality for other interfaces
from src.misc.interface_strings import RETURN                             # Import the RETURN namespace, containing strings or configurations for the return interface

class ReturnInterface(BaseInterface):
    """
    Interface for returning rented vehicles.
    
    Allows users to:
    - Enter return details (kilometers driven and late days)
    - Calculate and process the total return cost
    """
    
    def __init__(self, on_return_home, system):
        """Initialize the return interface with vehicle list and event bindings.
        
        Args:
            on_return_home (Callable): Function used to go back to main menu interface
            system (System): Reference to the application's System instance
        """
        super().__init__(*RETURN.TITLES, system=system)                                 # Initializes 'BaseInterface' with the pre-defined TITLES strings

        has_content = self.load_content(                                                # Executes necessary module to extract database content and display it accordingly; receives boolean indicating if content was found or not
                headers=RETURN.HEADERS,                                                 # Parameter for set of strings that will be displayed at the very top (column names)
                get_content=self.system.get_unavailable_vehicles,                       # Function to fetch content from database
                generate_model=RETURN.GENERATE_MODEL,                                   # Function which defines how each piece of data should be displayed
                empty_message=RETURN.EMPTY_MESSAGE                                      # Message if no content is found
            )

        if has_content:                                                                 # Checks if content was available
            action_number = self.input_loop(RETURN.VALIDATOR, RETURN.LOOP_MESSAGE)      # Activates loop with validating callable and message to display, then assigns the (cleaned) user input
            if action_number == 1:                                                      # Check if allowed action was chosen
                self.return_vehicle()                                                   # Executes chosen action if condition is met
        
        on_return_home()                                      # Returns to main menu

    def return_vehicle(self):
        """
        Opens a dialog window for returning a vehicle.
        
        Displays vehicle details and provides input fields for:
        - Kilometers driven
        - Late return days
        
        Args:
            vehicle_id (int): The ID of the vehicle being returned.
        """
        try:
            vehicle_id = abs(int(input("Vehicle ID: ")))
            customer_name = self.system.get_customer_name(vehicle_id)                               # Retrieve customer name associated with the vehicle

            if not customer_name:
                raise ValueError
            
            print("Customer Name: ", customer_name)

            actual_km = abs(int(input("Kilometers Driven: ")))                                        # Convert kilometers driven to integer
            late_days = abs(int(input("Late Days: ")))                                                # Convert late days to integer
        except ValueError:
            print("Invalid values, please try again.\n")
            return

        total_cost = self.system.query_return(vehicle_id, customer_name, actual_km, late_days)  # Calculate total cost

        if total_cost:
            print(f"Vehicle returned! Total cost: €{total_cost}\n")                          # Show confirmation message    
        else:
            print("Vehicle not found or already returned.\n")                           # Show error if vehicle return fails