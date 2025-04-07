from src.pages.interfaces.base_interface import BaseInterface       # Import the BaseInterface class, which serves as a parent class for other interfaces
from src.misc.interface_strings import INVENTORY                    # Import the INVENTORY namespace, which contains strings or configurations related to the inventory interface

class InventoryInterface(BaseInterface):
    """
    Represents the interface for showcasing all the existing vehicles in the database.
    Inherits components from BaseInterface.
    """
    def __init__(self, on_return_home, system):
        """Initialize the inventory interface.
        
        Args:
            on_return_home (Callable): Function used to go back to main menu interface
            system (System): Reference to the application's System instance
        """
        super().__init__(*INVENTORY.TITLES, system=system)                                      # Initializes 'BaseInterface' with the pre-defined TITLES strings

        self.load_content(                                                                      # Executes necessary modules to extract database content and display it accordingly
            headers=INVENTORY.HEADERS,                                                          # Set of strings that will be displayed at the very top (column names)
            get_content=self.system.vehicles,                                                   # Enters function to extract database content
            generate_model=INVENTORY.GENERATE_MODEL,                                            # Enters string generator for each listbox row
            empty_message=INVENTORY.EMPTY_MESSAGE,                                              # Message to be displayed in case no content is found
        )
        
        action_number = self.input_loop(INVENTORY.VALIDATOR, INVENTORY.LOOP_MESSAGE)            # Activates loop with validating callable and message to display, then assigns the (cleaned) user input
        if action_number == 1:                                                                  # Check if allowed action was chosen
            self.add_vehicle()                                                                  # Executes chosen action if condition is met
        
        on_return_home()                                                                        # Returns to main menu

    def add_vehicle(self):
        """Shows controlled input to add a new vehicle to the database.
        
        Creates a series of input components requesting the entry fields for:
        - Brand
        - Model 
        - Mileage
        - Daily price
        - Maintenance cost
        
        Includes validation and submission functionality.
        """
        try:                                                                            # Creates scope to handle any errors
            brand = str(input("Brand: "))                                               # Turns 'brand' param to an integer if possible, or raises an error
            model = str(input("Model: "))                                               # Turns 'model' param to an integer if possible, or raises an error
            current_mileage = abs(int(input("Mileage: ")))                              # Turns 'current_mileage' param to an integer if possible, or raises an error
            daily_price = abs(float(input("Daily Price: ")))                            # Turns 'daily_price' param to a float if possible, or raises an error
            maintenance_cost = abs(float(input("Maintenance Cost: ")))                  # Turns 'maintenance_cost' param to a float if possible, or raises an error

            if not all([brand, model]):                                                 # Checks that string values entered are acceptable
                raise ValueError()                                                      # Raises exception and stops code execution

            self.system.add_vehicle(                                                    # Calls system's module to add a vehicle to the database with all the information
                brand=brand,                                                            # Sets parameter by key
                model=model,                                                            # Sets parameter by key
                current_mileage=current_mileage,                                        # Sets parameter by key
                daily_price=daily_price,                                                # Sets parameter by key
                maintenance_cost=maintenance_cost                                       # Sets parameter by key
            )
            print("Vehicle added successfully!\n")                                      # Displays success message
        except ValueError:                                                              # If any of the values is something that it should not, the code skips to here
            print("Invalid values, please try again.\n")                                # Print error    