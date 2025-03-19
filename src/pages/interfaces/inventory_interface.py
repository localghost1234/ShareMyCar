import tkinter as tk                                                # Import the tkinter library for creating the GUI, aliased as 'tk' for convenience
from src.pages.interfaces.base_interface import BaseInterface       # Import the BaseInterface class, which serves as a parent class for other interfaces
from src.misc.strings import INVENTORY                              # Import the INVENTORY constant, which contains strings or configurations related to the inventory interface

class InventoryInterface(BaseInterface):
    """
        Represents the interface for showcasing all the existing vehicles in the database.
        Inherits components from BaseInterface
    """
    def __init__(self, root, system):
        super().__init__(root,  system, *INVENTORY.TITLES)                                          # Initializes 'BaseInterface' with the pre-defined TITLES strings

        self.create_scrollable_listbox(INVENTORY.HEADERS)                                           # Initializes the Listbox with the column names

        self.refresh_listbox = lambda: (                                                            # Creates an executable function to be used around interface
            self.load_content(                                                                      # Executes necessary modules to extract database content and display it accordingly
                get_content=self.system.get_all_vehicles,                                           # Enters function to extract database content
                generate_model=INVENTORY.GENERATE_MODEL,                                            # Enters string generator for each listbox row
                empty_message=INVENTORY.EMPTY_MESSAGE,                                              # Message to be displayed in case no content is found
            )
        )

        self.refresh_listbox()                                                                      # Loads content using locally created callback

        tk.Button(self.frame, text="Add Vehicle", command=self.add_vehicle).pack(padx=10, pady=10)  # Sets a button with necessary command and positions it

    def add_vehicle(self):
        """Opens modal window to add a new vehicle to the database."""
        modal_window = tk.Toplevel(self.frame)                                                  # Creates a modal where all the necessary components will be shown
        modal_window.title("Add Vehicle")                                                       # Adds a name to it
        modal_window.geometry("300x200")                                                        # Sets its size

        tk.Label(modal_window, text="Brand:").grid(row=0, column=0, padx=10, pady=5)            # Adds a text string and positions it
        brand_entry = tk.Entry(modal_window)                                                    # Adds a component where input can be given and links it to the current modal
        brand_entry.grid(row=0, column=1, padx=10, pady=5)                                      # Positions the Entry component

        tk.Label(modal_window, text="Model:").grid(row=1, column=0, padx=10, pady=5)            # Adds a text string and positions it
        model_entry = tk.Entry(modal_window)                                                    # Adds a component where input can be given and links it to the current Frame
        model_entry.grid(row=1, column=1, padx=10, pady=5)                                      # Positions the Entry component

        tk.Label(modal_window, text="Mileage:").grid(row=2, column=0, padx=10, pady=5)          # Adds a text string and positions it
        mileage_entry = tk.Entry(modal_window)                                                  # Adds a component where input can be given and links it to the current Frame
        mileage_entry.grid(row=2, column=1, padx=10, pady=5)                                    # Positions the Entry component

        tk.Label(modal_window, text="Daily Price:").grid(row=3, column=0, padx=10, pady=5)      # Adds a text string and positions it
        daily_price_entry = tk.Entry(modal_window)                                              # Adds a component where input can be given and links it to the current Frame
        daily_price_entry.grid(row=3, column=1, padx=10, pady=5)                                # Positions the Entry component

        tk.Label(modal_window, text="Maintenance Cost:").grid(row=4, column=0, padx=10, pady=5) # Adds a text string and positions it
        maintenance_cost_entry = tk.Entry(modal_window)                                         # Adds a component where input can be given and links it to the current Frame
        maintenance_cost_entry.grid(row=4, column=1, padx=10, pady=5)                           # Positions the Entry component

        def extract_data_and_submit():                                                          # Defines in-scope function to then add it to the Button
            self.submit_vehicle(                                                                # Uses local callback function
                brand_entry.get(),                                                              # Delivers content in Entry component
                model_entry.get(),                                                              # Delivers content in Entry component
                mileage_entry.get(),                                                            # Delivers content in Entry component
                daily_price_entry.get(),                                                        # Delivers content in Entry component
                maintenance_cost_entry.get(),                                                   # Delivers content in Entry component
                modal_window,                                                                   # Gives a reference to the current modal
            )

        tk.Button(modal_window, text="Submit", command=extract_data_and_submit).grid(row=5, column=0, columnspan=2, pady=10)  # Creates a Button, adds functionality, and positions it around the modal

    def submit_vehicle(self, brand, model, mileage, daily_price, maintenance_cost, modal):
        """
            Submits the new vehicle data to the system and updates the interface.

            Args:
                brand (str): The brand of the vehicle.
                model (str): The model of the vehicle.
                mileage (str): The mileage of the vehicle.
                daily_price (str): The daily rental price of the vehicle.
                maintenance_cost (str): The maintenance cost per kilometer of the vehicle.
                modal (tk.Toplevel): The modal window to be closed after submission.
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

        modal.destroy()                                                                         # Modal for adding vehicles is destroyed
        self.refresh_listbox()                                                                  # Uses local callback to reload all the new info