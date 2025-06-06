from types import SimpleNamespace               # Brings the namespace module to be used here, which helps us identify variables

HOME=SimpleNamespace(                                                   # Variable with strings to be used in HomeInterface
    TITLE="Welcome to the car sharing management system!",              # Message to be displayed at the top of interface
    VALIDATOR=lambda num: num < 1 or num > 8,                           # When entering a loop, it will check if the user input fits the instructions
    LOOP_MESSAGE = """Please select a valid operation (1-6):
            1) Check Vehicle Inventory
            2) Book A Vehicle
            3) Return A Vehicle
            4) Check Vehicle Maintenance
            5) Check Logs
            6) Check Financial Metrics
            7) Close the program

            """                                                         # When entering a loop, these instructions will be displayed for the user
)

INVENTORY=SimpleNamespace(                                                                                          # Variable with strings to be used in InventoryInterface
    TITLES = ("Inventory Management", "All existing vehicles:"),                                                    # Title and subtitle of interface
    HEADERS = ("Vehicle ID", "Brand", "Model", "Mileage (kms)", "Daily Price", "Maintenance Cost", "Available"),    # Column names shown on top of displayed data
    EMPTY_MESSAGE = "No vehicles in existence.",                                                                    # Message displayed when no data is found
    GENERATE_MODEL = lambda content: (                                                                              # Function used to generate strings of rows with the provided data
        f"{content.get('id'):<15} | "                                                                               # Formatted strings to take in content and add at least 13 blank spaces, regardless of string size
        f"{content.get('brand'):<15} | "
        f"{content.get('model'):<15} | "
        f"{content.get('current_mileage'):<15} | "
        f"€{content.get('daily_price'):<15} | "
        f"€{content.get('maintenance_cost'):<15} | "
        f"{'Yes' if content.get('available') else 'No':<15}"
    ),
    VALIDATOR = lambda num: num < 1 or num > 2,                                                                     # When entering a loop, it will check if the user input fits the instructions
    LOOP_MESSAGE = """Choose an action:
                    1) Add Vehicle
                    2) Back to main menu
                    
                    """                                                                                             # When entering a loop, these instructions will be displayed for the user
)

BOOKING=SimpleNamespace(                                                                # Variable with strings to be used in BookingInterface
    TITLES=("Booking Management", "Provide data or press 'Enter' to cancel.")           # Title and subtitle of interface
)

RETURN=SimpleNamespace(                                                                                 # Variable with strings to be used in ReturnInterface
    TITLES = ("Return Management", "Select a booked vehicle:"),                                         # Title and subtitle of interface
    HEADERS = ("Vehicle ID", "Brand", "Model", "Mileage", "Daily Price", "Maintenance Cost"),           # Column names shown on top of displayed data
    EMPTY_MESSAGE = "No booked vehicles found.",                                                        # Message displayed when no data is found
    GENERATE_MODEL = lambda content: (                                                                  # Function used to generate strings of rows with the provided data; data is segmented 
        f"{content.get('id'):<15} | "                                                                   # Formatted strings to take in content and add at least 15 blank spaces, regardless of string size
        f"{content.get('brand'):<15} | "
        f"{content.get('model'):<15} | "
        f"{content.get('current_mileage'):<15} | "
        f"€{content.get('daily_price'):<15} | "
        f"€{content.get('maintenance_cost'):<15}"
    ),
    VALIDATOR = lambda num: num < 1 or num > 2,                                                         # When entering a loop, it will check if the user input fits the instructions
    LOOP_MESSAGE = """Choose an action:
                1) Return Vehicle
                2) Back to main menu
                
                """                                                                                     # When entering a loop, these instructions will be displayed for the user
)

MAINTENANCE=SimpleNamespace(                                                                # Variable with strings to be used in MaintenanceInterface
    TITLES = ("Maintenance Management", "Select a vehicle needing maintenance:"),           # Title and subtitle of interface
    HEADERS = ("Vehicle ID", "Brand", "Model", "Current Mileage", "Maintenance Cost"),      # Column names shown on top of displayed data
    EMPTY_MESSAGE = "All vehicles are in good condition.",                                  # Message displayed when no data is found
    GENERATE_MODEL = lambda content: (                                                      # Function used to generate strings of rows with the provided data
        f"{content.get('id'):<15} | "                                                       # Formatted strings to take in content and add at least 10 blank spaces, regardless of string size
        f"{content.get('brand'):<15} | "
        f"{content.get('model'):<15} | "
        f"{content.get('current_mileage'):<15} | "
        f"€{content.get('maintenance_cost'):<15}"
    ),
    VALIDATOR = lambda num: num < 1 or num > 2,                                             # When entering a loop, it will check if the user input fits the instructions
    LOOP_MESSAGE = """Choose an action:
                    1) Remove vehicle from list
                    2) Return to main menu
                    
                    """                                                                     # When entering a loop, these instructions will be displayed for the user
)

LOGS=SimpleNamespace(                                                                                                                           # Variable with strings to be used in LogsInterface
    TITLES = ("Logs Management", "Transaction Logs"),                                                                                           # Title and subtitle of interface
    HEADERS = ("Log ID", "Vehicle ID", "Customer Name", "Rental Duration (Days)", "Revenue (€)", "Additional Costs (€)", "Transaction Type"),   # Column names shown on top of displayed data
    EMPTY_MESSAGE = "No transaction logs found.",                                                                                               # Message displayed when no data is found
    GENERATE_MODEL = lambda content: (                                                                                                          # Function used to generate strings of rows with the provided data
        f"{content.get('id'):<15} | "                                                                                                           # Formatted strings to take in content and add at least 15 blank spaces, regardless of string size
        f"{content.get('vehicle_id'):<15} | "
        f"{content.get('customer_name'):<15} | "
        f"{content.get('rental_duration'):<15} | "
        f"€{content.get('revenue'):<15} | "
        f"€{content.get('additional_costs'):<15} | "
        f"{content.get('transaction_type'):<15}"
    )
)

METRICS=SimpleNamespace(                                                                                                                # Variable with strings to be used in MetricsInterface
    TITLES = ("Metrics Management", "Financial Metrics"),                                                                               # Title and subtitle of interface
    HEADERS = ("Total Revenue (€)", "Total Operational Costs (€)", "Total Profit (€)", "Average Mileage (km/vehicle)"),                 # Column names shown on top of displayed data
    EMPTY_MESSAGE = "No financial data available.",                                                                                     # Message displayed when no data is found
    PDF_HEADERS=SimpleNamespace(                                                                                                        # Column names used when displaying data in the PDFs
        VEHICLES = ("Vehicle ID", "Brand", "Model", "Mileage", "Daily Price", "Maintenance Cost", "Available", "Maintenance Mileage"),  # Column names for the 'vehicles' table
        BOOKINGS = ("Booking ID", "Vehicle ID", "Rental Duration (Days)", "Estimated KM", "Estimated Cost", "Customer Name"),           # Column names for the 'bookings' table
        LOGS = ("Log ID", "Vehicle ID", "Rental Duration (Days)", "Revenue", "Additional Costs", "Customer Name", "Transaction Type"),  # Column names for the 'logs' table
    ),
    VALIDATOR = lambda num: num < 1 or num > 3,                                                                                         # When entering a loop, it will check if the user input fits the instructions
    LOOP_MESSAGE = """Please choose a valid operation:
        1) Make Query
        2) Download Full Report
        3) Return to main menu

        """                                                                                                                             # When entering a loop, these instructions will be displayed for the user
)