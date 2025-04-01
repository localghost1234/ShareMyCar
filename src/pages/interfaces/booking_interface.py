from src.pages.interfaces.base_interface import BaseInterface       # Import the BaseInterface class, which serves as a parent class for other interfaces
from src.misc.strings import BOOKING                                # Import the BOOKING namespace, which contains strings or configurations related to the booking interface

class BookingInterface(BaseInterface):
    """
    This interface allows the user to enter which vehicle (if available) to rent.
    
    To make a booking, the user must enter:
    - Vehicle ID
    - Customer's name
    - Estimated rent duration (in days)
    - Estimated kilometers to be driven
    
    Attributes:
        vehicle_id_entry (tk.Entry): Input field for vehicle ID
        customer_name_entry (tk.Entry): Input field for customer name
        rental_days_entry (tk.Entry): Input field for rental duration
        estimated_km_entry (tk.Entry): Input field for estimated kilometers
    """
    def __init__(self, on_switch_interface, system):
        """Initialize the booking interface with input fields and booking button.
        
        Args:
            system: Reference to the application's System instance
        """
        super().__init__(system, BOOKING.TITLE)                                           # Initializes 'BaseInterface' with the pre-defined TITLES strings

        self.vehicle_id_entry = input("Vehicle ID: ")                                                           # Adds a text string and positions it
        self.customer_name_entry = input("Customer Name: ")                                                           # Adds a text string and positions it
        self.rental_duration_entry = input("Rental Duration (days): ")                                                       # Adds a text string and positions it
        self.estimated_km_entry = input("Estimated Kilometers: ")                                               # Adds a text string and positions it

        self.create_booking()
        on_switch_interface(0)

    def create_booking(self):
        """Handles booking process by taking input values and calling system logic.
        
        Validates input fields and attempts to create a booking through the system.
        Displays appropriate success/error messages to the user.
        """
        try:                                                                                    # Creates a scope where errors get handled accordingly
            vehicle_id = int(self.vehicle_id_entry)                                       # Turns 'vehicle_id_entry' input into an integer, or raises an error
            customer_name = str(self.customer_name_entry)                                 # Turns 'customer_name_entry' input into a float, or raises an error
            rental_days = int(self.rental_duration_entry)                                     # Turns 'rental_days_entry' input into an integer, or raises an error
            estimated_km = int(self.estimated_km_entry)                                   # Turns 'estimated_km_entry' input into an integer, or raises an error
        except ValueError:
            print("Please enter valid values\n")
            return
        
        cost = 0.0                                                                                  # Initialize 'cost' variable outside the scope

        try:                                                                                        # Creates error handling scope
            cost = self.system.query_booking(vehicle_id, rental_days, estimated_km, customer_name)  # Calls the system variable's function to add a booking to the database; returns the cost of said booking
        except Exception as err:                                                                    # If error is found, this block is executed
            print("Error in 'query_booking()'\n", err)                                              # Displays message on developer's console

        if cost:                                                                                    # Checks if the returned value is truthy (cost should always be above 0) 
            print(f"Vehicle booked! Estimated cost: €{cost}\n")                              # Displays success modal with calculated cost for the client
        else:                                                                                       # Alternate condition, in case the former was falsy
            print("Vehicle not found or unavailable\n")                                    # Displays error modal