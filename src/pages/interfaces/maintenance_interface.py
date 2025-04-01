from src.pages.interfaces.base_interface import BaseInterface       # Import the BaseInterface class, a parent class providing common functionality for other interfaces
from src.misc.strings import MAINTENANCE                            # Import the MAINTENANCE namespace, containing strings or configurations for the maintenance interface

class MaintenanceInterface(BaseInterface):
    """ 
    Interface for managing vehicle maintenance.
    
    Displays vehicles requiring maintenance and allows:
    - Viewing maintenance-required vehicles
    - Updating maintenance status
    - Resetting maintenance mileage
    
    Inherits from BaseInterface for common functionality.
    
    Attributes:
        refresh_listbox (function): Callback to refresh the vehicle list
    """

    def __init__(self, on_switch_interface, system):
        """Initialize the maintenance interface with vehicle list and event bindings.
        
        Args:
            system: Reference to the application's System instance
        """
        super().__init__(system, *MAINTENANCE.TITLES)                             # Initializes 'BaseInterface' with the pre-defined TITLES strings

        self.refresh_listbox = lambda: (                                                # Creates an executable function to be used around interface
            self.load_content(                                                          # Loads the list with vehicles that need maintenance
                headers=MAINTENANCE.HEADERS,
                get_content=self.system.get_vehicles_requiring_maintenance,             # Function to fetch vehicles requiring maintenance
                generate_model=MAINTENANCE.GENERATE_MODEL,                              # Formatting function for vehicle data
                empty_message=MAINTENANCE.EMPTY_MESSAGE,                                # Message to display if no vehicles require maintenance
            )
        )

        self.refresh_listbox()                                                          # Loads content using locally created callback

    def show_maintenance_dialog(self, vehicle_id):
        """
        Displays confirmation dialog for completing vehicle maintenance.
        
        Args:
            vehicle_id (int): The ID of the vehicle to update
        """

        tk.Label(modal_window, text="Remove from maintenance list and update maintenance mileage?", font=("Arial", 11)).pack(pady=10)      # Label for vehicle ID
        
        button_frame = tk.Frame(modal_window)
        button_frame.pack()

        def confirm_maintenance_update(): # Defines in-scope function to then add it to the Button
            self.system.query_update_maintenance_mileage(vehicle_id)
            self.refresh_listbox()
            modal_window.destroy()

        tk.Button(button_frame, text="Yes", command=confirm_maintenance_update).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=lambda: (modal_window.destroy())).pack(side=tk.LEFT)