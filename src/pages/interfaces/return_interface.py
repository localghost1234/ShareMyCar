import tkinter as tk
from src.pages.interfaces.base_interface import BaseInterface
from src.misc.strings import RETURN

class ReturnInterface(BaseInterface):
    """
    Represents the interface for returning a vehicle in the rental system.
    
    This interface displays a list of currently unavailable vehicles and allows users
    to select a vehicle to return. A dialog prompts the user to enter the kilometers driven
    and late return days, then calculates the total return cost.
    
    Attributes:
        listbox (tk.Listbox): A scrollable list displaying unavailable vehicles.
    """
    
    def __init__(self, root, system):
        """
        Initializes the return interface.
        
        Args:
            root (tk.Tk or tk.Toplevel): The parent window for this interface.
            system: The backend system managing vehicle rentals.
        """
        super().__init__(root, system, *RETURN.TITLES)

        self.create_scrollable_listbox(RETURN.HEADERS, disable_clicking=False)  # Create a scrollable listbox for unavailable vehicles
        
        self.load_content(
            get_content=self.system.get_unavailable_vehicles,  # Fetch unavailable vehicles
            generate_model=RETURN.GENERATE_MODEL,  # Define how vehicle data is displayed
            empty_message=RETURN.EMPTY_MESSAGE  # Message if no vehicles are found
        )

        self.listbox.bind("<Double-Button-1>", self.on_vehicle_double_click)  # Bind double-click event to handle vehicle selection

    def on_vehicle_double_click(self, event):
        """
        Handles double-clicking on a vehicle in the list, extracting its ID and opening the return dialog.
        
        Args:
            event (tk.Event): The event triggered by the double-click.
        """
        selected_index = self.listbox.curselection()  # Get the selected item index
        
        if selected_index:
            selected_vehicle = self.listbox.get(selected_index)  # Get selected vehicle details
            vehicle_id = int(selected_vehicle.split(" | ")[0].strip())  # Extract vehicle ID from the list entry
            self.show_return_dialog(vehicle_id)  # Open return dialog with vehicle ID

    def show_return_dialog(self, vehicle_id):
        """
        Opens a dialog window for returning a vehicle, displaying its details and input fields for kilometers driven and late days.
        
        Args:
            vehicle_id (int): The unique identifier of the vehicle being returned.
        """
        customer_name = self.system.get_customer_name(vehicle_id)  # Retrieve customer name associated with the vehicle

        dialog = tk.Toplevel(self.root)  # Create a new top-level window
        dialog.title("Return Vehicle")  # Set window title
        dialog.geometry("300x200")  # Define window size

        tk.Label(dialog, text="Vehicle ID:").grid(row=0, column=0, padx=10, pady=5)  # Label for vehicle ID
        vehicle_id_entry = tk.Entry(dialog)  # Input field for vehicle ID
        vehicle_id_entry.insert(0, str(vehicle_id))  # Populate with the vehicle ID
        vehicle_id_entry.config(state=tk.DISABLED)  # Make it read-only
        vehicle_id_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(dialog, text="Customer Name:").grid(row=1, column=0, padx=10, pady=5)  # Label for customer name
        customer_name_entry = tk.Entry(dialog)  # Input field for customer name
        customer_name_entry.insert(0, customer_name)  # Populate with the customer's name
        customer_name_entry.config(state=tk.DISABLED)  # Make it read-only
        customer_name_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(dialog, text="Kilometers Driven:").grid(row=2, column=0, padx=10, pady=5)  # Label for kilometers driven
        actual_km_entry = tk.Entry(dialog)  # Input field for kilometers driven
        actual_km_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(dialog, text="Late Days:").grid(row=3, column=0, padx=10, pady=5)  # Label for late days
        late_days_entry = tk.Entry(dialog)  # Input field for late days
        late_days_entry.grid(row=3, column=1, padx=10, pady=5)

        submit_button = tk.Button(
            dialog, text="Submit",  # Submit button
            command=lambda: self.submit_return(
                vehicle_id, actual_km_entry.get(), late_days_entry.get(), customer_name, dialog
            )
        )
        submit_button.grid(row=4, column=0, columnspan=2, pady=10)  # Position submit button

    def submit_return(self, vehicle_id, actual_km, late_days, customer_name, dialog):
        """
        Validates the return details, calculates total cost, and updates the system.
        
        Args:
            vehicle_id (int): The ID of the vehicle being returned.
            actual_km (str): The actual kilometers driven (to be validated and converted to int).
            late_days (str): The number of late days (to be validated and converted to int).
            customer_name (str): The name of the customer returning the vehicle.
            dialog (tk.Toplevel): The return dialog window to be closed after processing.
        """
        try:
            actual_km = int(actual_km)  # Convert kilometers driven to integer
            late_days = int(late_days)  # Convert late days to integer
        except ValueError:
            self.show_error("Please enter valid numbers for kilometers and late days.")  # Display error for invalid input
            return

        total_cost = self.system.query_return(vehicle_id, actual_km, late_days, customer_name)  # Calculate total cost

        if total_cost:
            self.show_info(f"Vehicle returned! Total cost: €{total_cost}")  # Show confirmation message
            dialog.destroy()  # Close return dialog
            
            self.load_content(
                get_content=self.system.get_unavailable_vehicles,  # Refresh vehicle list
                generate_model=RETURN.GENERATE_MODEL,
                empty_message=RETURN.EMPTY_MESSAGE,
            )
        else:
            self.show_error("Vehicle not found or already returned.")  # Show error if vehicle return fails
