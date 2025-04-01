from src.pages.interfaces.base_interface import BaseInterface       # Import the BaseInterface class, which serves as a parent class for other interfaces
from src.misc.strings import INVENTORY                              # Import the INVENTORY namespace, which contains strings or configurations related to the inventory interface

class InventoryInterface(BaseInterface):
    """
    Represents the interface for showcasing all the existing vehicles in the database.
    Inherits components from BaseInterface.

    Attributes:
        refresh_listbox (function): Callback function to refresh the listbox content
    """
    def __init__(self, on_switch_interface, system):
        """Initialize the inventory interface.
        
        Args:
            system: Reference to the application's System instance
        """
        super().__init__(system, *INVENTORY.TITLES)                                                 # Initializes 'BaseInterface' with the pre-defined TITLES strings

        self.refresh_listbox = lambda: (                                                            # Creates an executable function to be used around interface
            self.load_content(                                                                      # Executes necessary modules to extract database content and display it accordingly
                headers=INVENTORY.HEADERS,
                get_content=self.system.get_all_vehicles,                                           # Enters function to extract database content
                generate_model=INVENTORY.GENERATE_MODEL,                                            # Enters string generator for each listbox row
                empty_message=INVENTORY.EMPTY_MESSAGE,                                              # Message to be displayed in case no content is found
            )
        )

        self.refresh_listbox()                                                                      # Loads content using locally created callback

        action_number = -1
        
        while action_number < 1 and action_number > 2:
            action_number = input(
                "Choose an action (1-2):\n"
                    "1) Add Vehicle\n"
                    "2) Exit\n\n"
                )  # Sets a button with necessary command and positions it

        if action_number == 1:
            add_vehicle()
        elif action_number == 2:
            on_switch_interface(0)

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
        brand_entry = input("Brand:")                                                           # Adds a text string and positions it
        model_entry = input("Model:")                                                           # Adds a text string and positions it
        mileage_entry = input("Mileage:")                                                       # Adds a text string and positions it
        daily_price_entry = input("Daily Price:")                                               # Adds a text string and positions it
        maintenance_cost_entry = input("Maintenance Cost:")                                     # Adds a text string and positions it

        self.submit_vehicle(                                                                    # Uses local callback function
            brand_entry,                                                                        # Delivers content in Entry component
            model_entry,                                                                        # Delivers content in Entry component
            mileage_entry,                                                                      # Delivers content in Entry component
            daily_price_entry,                                                                  # Delivers content in Entry component
            maintenance_cost_entry,                                                             # Delivers content in Entry component
        )
        
    def submit_vehicle(self, brand, model, mileage, daily_price, maintenance_cost):
        """
        Submits the new vehicle data to the system and updates the interface.

        Args:
            brand (str): The brand of the vehicle.
            model (str): The model of the vehicle.
            mileage (str): The mileage of the vehicle.
            daily_price (str): The daily rental price of the vehicle.
            maintenance_cost (str): The maintenance cost per kilometer of the vehicle.
            modal (tk.Toplevel): The modal window to be closed after submission.
            
        Performs validation on all inputs before submitting to the system.
        Shows appropriate error messages if validation fails.
        """
        if not brand or not model or not mileage or not daily_price or not maintenance_cost:    # Checks whether any of the Entry components is empty
            self.show_error("All fields are required.")                                         # Display modal with error message
            return                                                                              # Stops further code execution

        try:                                                                                    # Creates scope to handle any errors
            mileage = int(mileage)                                                              # Turns 'mileage' param to an integer if possible, or raises an error
            daily_price = float(daily_price)                                                    # Turns 'daily_price' param to a float if possible, or raises an error
            maintenance_cost = float(maintenance_cost)                                          # Turns 'maintenance_cost' param to a float if possible, or raises an error
        except ValueError:                                                                      # If any of the values is something that it should not, the code skips to here
            self.show_error("Please enter valid values.")                                       # An error modal is displayed
            return                                                                              # Stops further code execution

        self.system.add_vehicle(brand, model, mileage, daily_price, maintenance_cost)           # Calls system's module to add a vehicle to the database with all the information
        self.show_info("Vehicle added successfully!")                                           # Displays success message

        self.refresh_listbox()                                                                  # Uses local callback to reload all the new info