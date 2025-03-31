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

    def __init__(self, root, system):
        """Initialize the maintenance interface with vehicle list and event bindings.
        
        Args:
            root (tk.Tk): The root window
            system: Reference to the application's System instance
        """
        super().__init__(root, system, *MAINTENANCE.TITLES)                             # Initializes 'BaseInterface' with the pre-defined TITLES strings

        self.create_scrollable_listbox(MAINTENANCE.HEADERS, disable_clicking=False)     # Sets a Listbox component with the column names of the displayed info
        self.refresh_listbox = lambda: (                                                # Creates an executable function to be used around interface
            self.load_content(                                                          # Loads the list with vehicles that need maintenance
                get_content=self.system.get_vehicles_requiring_maintenance,             # Function to fetch vehicles requiring maintenance
                generate_model=MAINTENANCE.GENERATE_MODEL,                              # Formatting function for vehicle data
                empty_message=MAINTENANCE.EMPTY_MESSAGE,                                # Message to display if no vehicles require maintenance
            )
        )

        self.refresh_listbox()                                                          # Loads content using locally created callback
        self.listbox.bind("<Double-Button-1>", self.on_vehicle_double_click)            # Bind double-click event to handle vehicle selection

    def on_vehicle_double_click(self, event):
        """
        Handles double-click events on maintenance-required vehicles.
        
        Extracts vehicle ID from selection and opens maintenance dialog.
        
        Args:
            event (tk.Event): The mouse click event object
        """
        selected_index = self.listbox.curselection()                        # Get the selected item index
        
        if selected_index:
            selected_vehicle = self.listbox.get(selected_index)             # Get selected vehicle details
            vehicle_id = int(selected_vehicle.split(" | ")[0].strip())      # Extract vehicle ID from the list entry
            self.show_maintenance_dialog(vehicle_id)                        # Open maintenance dialog with vehicle ID

    def show_maintenance_dialog(self, vehicle_id):
        """
        Displays confirmation dialog for completing vehicle maintenance.
        
        Args:
            vehicle_id (int): The ID of the vehicle to update
        """
        modal_window = tk.Toplevel(self.frame)                                                                                                     # Create a new modal window
        modal_window.title("Maintenance Checkup")                                                                                                  # Set window title
        modal_window.geometry("500x100")                                                                                                          # Define window size

        tk.Label(modal_window, text="Remove from maintenance list and update maintenance mileage?", font=("Arial", 11)).pack(pady=10)      # Label for vehicle ID
        
        button_frame = tk.Frame(modal_window)
        button_frame.pack()

        def confirm_maintenance_update(): # Defines in-scope function to then add it to the Button
            self.system.query_update_maintenance_mileage(vehicle_id)
            self.refresh_listbox()
            modal_window.destroy()

        tk.Button(button_frame, text="Yes", command=confirm_maintenance_update).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=lambda: (modal_window.destroy())).pack(side=tk.LEFT)