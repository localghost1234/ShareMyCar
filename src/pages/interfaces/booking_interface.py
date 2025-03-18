import tkinter as tk                                                # Import the tkinter library for creating the GUI, aliased as 'tk' for convenience
from src.pages.interfaces.base_interface import BaseInterface       # Import the BaseInterface class, which serves as a parent class for other interfaces
from src.misc.strings import BOOKING                                # Import the BOOKING constant, which contains strings or configurations related to the booking interface

class BookingInterface(BaseInterface):
    """
        This interface allows the user to enter which vehicle (if available) to rent.
        In order make a booking, the user must enter:
        - Vehicle ID
        - Customer's name
        - Estimated rent duration (in days)
        - Estimated kilometers to be driven
    """
    def __init__(self, root, system):
        super().__init__(root, system, BOOKING.TITLE)                                           # Initializes 'BaseInterface' with the pre-defined TITLES strings

        tk.Label(self.frame, text="Vehicle ID:", font=("Arial", 12)).pack(pady=5)               # Displays, stylizes and positions text on the Frame
        self.vehicle_id_entry = tk.Entry(self.frame)                                            # Sets Entry component to receive user input
        self.vehicle_id_entry.pack()                                                            # Positions the Entry component relative to the other components

        tk.Label(self.frame, text="Customer Name:", font=("Arial", 12)).pack(pady=5)            # Displays, stylizes and positions text on the Frame
        self.customer_name_entry = tk.Entry(self.frame)                                         # Sets Entry component to receive user input
        self.customer_name_entry.pack()                                                         # Positions the Entry component relative to the other components

        tk.Label(self.frame, text="Rental Duration (days):", font=("Arial", 12)).pack(pady=5)   # Displays, stylizes and positions text on the Frame
        self.rental_days_entry = tk.Entry(self.frame)                                           # Sets Entry component to receive user input
        self.rental_days_entry.pack()                                                           # Positions the Entry component relative to the other components

        tk.Label(self.frame, text="Estimated Kilometers:", font=("Arial", 12)).pack(pady=5)     # Displays, stylizes and positions text on the Frame
        self.estimated_km_entry = tk.Entry(self.frame)                                          # Sets Entry component to receive user input
        self.estimated_km_entry.pack()                                                          # Positions the Entry component relative to the other components

        tk.Button(self.frame, text="Book Vehicle", command=self.create_booking).pack(pady=25)   # Sets Button component, positions it, and adds actions it will execute

    def create_booking(self):
        """Handles booking process by taking input values and calling system logic."""
        try:                                                                                    # Creates a scope where errors get handled accordingly
            vehicle_id = int(self.vehicle_id_entry.get())                                       # Turns 'vehicle_id_entry' input into an integer, or raises an error
            rental_days = int(self.rental_days_entry.get())                                     # Turns 'rental_days_entry' input into an integer, or raises an error
            estimated_km = int(self.estimated_km_entry.get())                                   # Turns 'estimated_km_entry' input into an integer, or raises an error
            customer_name = str(self.customer_name_entry.get())                                 # Turns 'customer_name_entry' input into a float, or raises an error
        except ValueError:
            self.show_error("Please enter valid values.")
            return
        
        cost = 0.0                                                                              # Initialize 'cost' variable outside the scope

        try:                                                                                        # Creates error handling scope
            cost = self.system.query_booking(vehicle_id, rental_days, estimated_km, customer_name)  # Calls the system variable's function to add a booking to the database; returns the cost of said booking
        except Exception as err:                                                                    # If error is found, this block is executed
            print("Error in 'query_booking()'\n", err)                                              # Displays message on developer's console

        if cost:                                                                                # Checks if the returned value is truthy (cost should always be above 0) 
            self.show_info(f"Vehicle booked! Estimated cost: €{cost}")                          # Displays success modal with calculated cost for the client
        else:                                                                                   # Alternate condition, in case the former was falsy
            self.show_error("Vehicle not found or unavailable.")                                # Displays error modal
