from src.pages.interfaces.base_interface import BaseInterface   # Import the BaseInterface class, a parent class providing common functionality for other interfaces
from src.misc.strings import RETURN                             # Import the RETURN namespace, containing strings or configurations for the return interface
from src.misc.utilities import input_loop

class ReturnInterface(BaseInterface):
    """
    Interface for returning rented vehicles.
    
    Displays a list of currently unavailable vehicles and allows users to:
    - Select vehicles by double-clicking
    - Enter return details (kilometers driven and late days)
    - Calculate and process the total return cost
    
    Attributes:
        refresh_listbox (function): Callback to refresh the vehicle list
    """
    
    def __init__(self, on_switch_interface, system):
        """Initialize the return interface with vehicle list and event bindings.
        
        Args:
            system: Reference to the application's System instance
        """
        super().__init__(system, *RETURN.TITLES)                                  # Initializes 'BaseInterface' with the pre-defined TITLES strings

        self.refresh_listbox = lambda: (                                                # Creates an executable function to be used around interface
            self.load_content(                                                          # Executes necessary modules to extract database content and display it accordingly
                headers=RETURN.HEADERS,
                get_content=self.system.get_unavailable_vehicles,                       # Fetch unavailable vehicles
                generate_model=RETURN.GENERATE_MODEL,                                   # Define how vehicle data is displayed
                empty_message=RETURN.EMPTY_MESSAGE                                      # Message if no vehicles are found
            )
        )

        self.refresh_listbox()                                                          # Loads content using locally created callback

        is_valid = lambda num: num < 1 or num > 2
        message = """Choose an action:
                        1) Return Vehicle
                        2) Back to main menu
                        
                        """
        
        action_number = input_loop(is_valid, message)

        if action_number == 1:
            self.return_vehicle()

        on_switch_interface(0)

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
            vehicle_id = int(input("Vehicle ID: "))
            customer_name = self.system.get_customer_name(vehicle_id)                           # Retrieve customer name associated with the vehicle
            print("Customer Name:", customer_name)

            actual_km = int(input("Kilometers Driven:"))                                        # Convert kilometers driven to integer
            late_days = int(input("Late Days:"))                                                # Convert late days to integer
        except ValueError:
            print("Please enter valid numbers for kilometers and late days.")         # Display error for invalid input
            return

        total_cost = self.system.query_return(vehicle_id, customer_name, actual_km, late_days)  # Calculate total cost

        if not total_cost:
            print("Vehicle not found or already returned.")                           # Show error if vehicle return fails
            return
        
        print(f"Vehicle returned! Total cost: €{total_cost}")                          # Show confirmation message
        self.refresh_listbox()                                                                  # Uses local callback to reload all the new info
        