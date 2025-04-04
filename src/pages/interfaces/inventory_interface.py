from src.pages.interfaces.base_interface import BaseInterface       # Import the BaseInterface class, which serves as a parent class for other interfaces
from src.misc.interface_strings import INVENTORY                              # Import the INVENTORY namespace, which contains strings or configurations related to the inventory interface
from src.misc.utilities import input_loop
import time

class InventoryInterface(BaseInterface):
    """
    Represents the interface for showcasing all the existing vehicles in the database.
    Inherits components from BaseInterface.

    Attributes:
        refresh_list (function): Callback function to refresh the listbox content
    """
    def __init__(self, on_return_home, system):
        """Initialize the inventory interface.
        
        Args:
            system: Reference to the application's System instance
        """
        super().__init__(system, *INVENTORY.TITLES)                                                 # Initializes 'BaseInterface' with the pre-defined TITLES strings

        self.refresh_list = lambda: (                                                            # Creates an executable function to be used around interface
            self.load_content(                                                                      # Executes necessary modules to extract database content and display it accordingly
                headers=INVENTORY.HEADERS,
                get_content=self.system.get_all_vehicles,                                           # Enters function to extract database content
                generate_model=INVENTORY.GENERATE_MODEL,                                            # Enters string generator for each listbox row
                empty_message=INVENTORY.EMPTY_MESSAGE,                                              # Message to be displayed in case no content is found
            )
        )

        self.refresh_list()                                                                      # Loads content using locally created callback

        is_valid = lambda num: num < 1 or num > 2
        message = """Choose an action:
                        1) Add Vehicle
                        2) Back to main menu
                        
                        """
        
        action_number = input_loop(is_valid, message)

        if action_number == 1:
            self.add_vehicle()
        
        on_return_home()

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
        brand = input("Brand: ")                                                           # Adds a text string and positions it
        model = input("Model: ")                                                           # Adds a text string and positions it
        current_mileage = input("Mileage: ")                                                       # Adds a text string and positions it
        daily_price = input("Daily Price: ")                                               # Adds a text string and positions it
        maintenance_cost = input("Maintenance Cost: ")                                     # Adds a text string and positions it

        try:                                                                                    # Creates scope to handle any errors
            brand = str(brand)
            model = str(model)
            current_mileage = int(current_mileage)                                                              # Turns 'current_mileage' param to an integer if possible, or raises an error
            daily_price = float(daily_price)                                                    # Turns 'daily_price' param to a float if possible, or raises an error
            maintenance_cost = float(maintenance_cost)                                          # Turns 'maintenance_cost' param to a float if possible, or raises an error
        except ValueError:                                                                      # If any of the values is something that it should not, the code skips to here
            print("Invalid values, please try again.\n")
            time.sleep(2)
            return                                                                              # Stops further code execution

        self.system.add_vehicle(brand, model, current_mileage, daily_price, maintenance_cost)           # Calls system's module to add a vehicle to the database with all the information
        print("Vehicle added successfully!")                                           # Displays success message
    