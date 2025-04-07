from src.pages.interfaces.base_interface import BaseInterface             # Import the BaseInterface class, a parent class providing common functionality for other interfaces
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
        
        on_return_home()                                                                # Returns to main menu

    def return_vehicle(self):
        """
        Opens a dialog window for returning a vehicle.
        
        Displays vehicle details and provides input fields for:
        - Kilometers driven
        - Late return days
        
        Args:
            vehicle_id (int): The ID of the vehicle being returned.
        """
        try:                                                                           # Creates a scope to catch any error during the process
            vehicle_id = abs(int(input("Vehicle ID: ")))                               # Obtains vehicle id from user input, and checks if it's a valid, positive integer
            customer_name = self.system.get_customer_name(vehicle_id)                  # Retrieve customer name associated with the vehicle

            if not customer_name:                                                      # If no record of a vehicle with that ID is found, customer_name will be falsy
                raise ValueError                                                       # Making use of the 'try-except' functionality, we send our execution to the end of the scope
            
            print("Customer Name: ", customer_name)                                    # Assuming the previous condition was not met, we display the customer's name

            actual_km = abs(int(input("Kilometers Driven: ")))                         # Obtain kilometers driven by the customer and ensure input is a positive integer
            late_days = abs(int(input("Late Days: ")))                                 # Obtain extra days after original duration estimation and ensure input is a positive integer
        except ValueError:                                                             # If any error is found, code skips to this line
            print("Invalid values, please try again.\n")                               # Print error message
            return                                                                     # Stop further code execution

        total_cost = self.system.query_return(                                         # Calculate total cost for the client
            vehicle_id=vehicle_id,                                                     # Sets parameter by key
            customer_name=customer_name,                                               # Sets parameter by key
            actual_km=actual_km,                                                       # Sets parameter by key
            late_days=late_days                                                        # Sets parameter by key
        )
        if total_cost != None:                                                         # Checks if the return was successful
            print(f"Vehicle returned! Total cost: €{total_cost}\n")                    # Show success message    
        else:                                                                          # Alternative if return was unsuccessful
            print("Vehicle not found or already returned.\n")                          # Show error message