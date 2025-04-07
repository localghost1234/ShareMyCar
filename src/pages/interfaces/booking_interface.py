from src.pages.interfaces.base_interface import BaseInterface       # Import the BaseInterface class, which serves as a parent class for other interfaces
from src.misc.interface_strings import BOOKING                      # Import the BOOKING namespace, which contains strings or configurations related to the booking interface

class BookingInterface(BaseInterface):
    """
    This interface allows the user to enter which vehicle (if available) to rent.
    
    To make a booking, the user must enter:
    - Vehicle ID
    - Customer's name
    - Estimated rent duration (in days)
    - Estimated kilometers to be driven
    """
    def __init__(self, on_return_home, system):
        """Initialize the booking interface with input fields and booking button.
        
        Args:
            on_return_home (Callable): Function used to go back to main menu interface
            system (System): Reference to the application's System instance
        """
        super().__init__(*BOOKING.TITLES, system=system)                                     # Initializes 'BaseInterface' with the pre-defined TITLES strings
        
        try:                                                                                            # Creates a scope to catch any error during execution
            vehicle_id = abs(int(input("Vehicle ID: ")))                                                # Adds a text string and positions it
            customer_name = str(input("Customer Name: "))                                               # Adds a text string and positions it
            rental_duration = abs(int(input("Rental Duration (days): ")))                               # Adds a text string and positions it
            estimated_km = abs(int(input("Estimated Kilometers: ")))                                    # Adds a text string and positions it
            
            print()                                                                                     # Line break to maintain readability
            cost = self.system.query_booking(vehicle_id, rental_duration, estimated_km, customer_name)  # Calls the system variable's function to add a booking to the database; returns the cost of said booking
            if cost:                                                                                    # Checks if the returned value is truthy (cost should always be above 0) 
                print(f"Vehicle booked! Estimated cost: €{cost}\n")                                     # Displays success modal with calculated cost for the client
            else:                                                                                       # Alternate condition, in case the former was falsy
                print("Vehicle not found or unavailable.\n")                                            # Displays error modal
        except ValueError:                                                                        # If any error occurs, code skips to this line
            print("Invalid values, please try again.\n")                                          # Print error and skip a line

        on_return_home()                                                                          # Return to main menu interface