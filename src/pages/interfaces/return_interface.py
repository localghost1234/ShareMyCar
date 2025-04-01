from src.pages.interfaces.base_interface import BaseInterface   # Import the BaseInterface class, a parent class providing common functionality for other interfaces
from src.misc.strings import RETURN                             # Import the RETURN namespace, containing strings or configurations for the return interface

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
                headers=MAINTENANCE.HEADERS,
                get_content=self.system.get_unavailable_vehicles,                       # Fetch unavailable vehicles
                generate_model=RETURN.GENERATE_MODEL,                                   # Define how vehicle data is displayed
                empty_message=RETURN.EMPTY_MESSAGE                                      # Message if no vehicles are found
            )
        )

        self.refresh_listbox()                                                          # Loads content using locally created callback

    def show_return_dialog(self, vehicle_id):
        """
        Opens a dialog window for returning a vehicle.
        
        Displays vehicle details and provides input fields for:
        - Kilometers driven
        - Late return days
        
        Args:
            vehicle_id (int): The ID of the vehicle being returned.
        """
        customer_name = self.system.get_customer_name(vehicle_id)                           # Retrieve customer name associated with the vehicle

        tk.Label(modal_window, text="Vehicle ID:").grid(row=0, column=0, padx=10, pady=5)          # Label for vehicle ID
        vehicle_id_entry = tk.Entry(modal_window)                                                  # Input field for vehicle ID
        vehicle_id_entry.insert(0, str(vehicle_id))                                                # Populate with the vehicle ID
        vehicle_id_entry.config(state=tk.DISABLED)                                                 # Make it read-only
        vehicle_id_entry.grid(row=0, column=1, padx=10, pady=5)                                    # Positions Entry object around the grid

        tk.Label(modal_window, text="Customer Name:").grid(row=1, column=0, padx=10, pady=5)       # Label for customer name
        customer_name_entry = tk.Entry(modal_window)                                               # Input field for customer name
        customer_name_entry.insert(0, customer_name)                                               # Populate with the customer's name
        customer_name_entry.config(state=tk.DISABLED)                                              # Make it read-only
        customer_name_entry.grid(row=1, column=1, padx=10, pady=5)                                 # Positions Entry object around the grid

        tk.Label(modal_window, text="Kilometers Driven:").grid(row=2, column=0, padx=10, pady=5)   # Label for kilometers driven
        actual_km_entry = tk.Entry(modal_window)                                                   # Input field for kilometers driven
        actual_km_entry.grid(row=2, column=1, padx=10, pady=5)                                     # Positions Entry object around the grid

        tk.Label(modal_window, text="Late Days:").grid(row=3, column=0, padx=10, pady=5)           # Label for late days
        late_days_entry = tk.Entry(modal_window)                                                   # Input field for late days
        late_days_entry.grid(row=3, column=1, padx=10, pady=5)                                     # Positions Entry object around the grid

        def extract_data_and_submit():                                                                                  # Defines in-scope function to then add it to the Button
            self.submit_return(vehicle_id, actual_km_entry.get(), late_days_entry.get(), customer_name, modal_window)   # Gets all data from Entries and runs submission logic
    
        tk.Button(modal_window, text="Submit", command=extract_data_and_submit).grid(row=4, column=0, columnspan=2, pady=10) # Creates and positions Button component with submission logic

    def submit_return(self, vehicle_id, actual_km, late_days, customer_name, modal):
        """
        Processes vehicle return by validating inputs and updating system records.
        
        Args:
            vehicle_id (int): The ID of the vehicle being returned
            actual_km (str): The kilometers driven (to be converted to int)
            late_days (str): The number of late days (to be converted to int)
            customer_name (str): The name of the customer
            modal (tk.Toplevel): The modal window to close after processing
            
        Returns:
            None: Shows success/error messages via popups rather than returning values
        """
        try:
            actual_km = int(actual_km)                                                          # Convert kilometers driven to integer
            late_days = int(late_days)                                                          # Convert late days to integer
        except ValueError:
            self.show_error("Please enter valid numbers for kilometers and late days.")         # Display error for invalid input
            return

        total_cost = self.system.query_return(vehicle_id, actual_km, late_days, customer_name)  # Calculate total cost

        if not total_cost:
            self.show_error("Vehicle not found or already returned.")                           # Show error if vehicle return fails
            return
        
        self.show_info(f"Vehicle returned! Total cost: €{total_cost}")                          # Show confirmation message
        modal.destroy()                                                                         # Close return dialog
        self.refresh_listbox()                                                                  # Uses local callback to reload all the new info