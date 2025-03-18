from types import SimpleNamespace                # Brings the namespace module to be used here, which helps us identify variables

INVENTORY=SimpleNamespace(                                                                                  # Variable with strings to be used in InventoryInterface
    TITLES = ("Inventory Management", "All existing vehicles"),                                             # Title and subtitle of interface
    HEADERS = ("ID", "Brand", "Model", "Mileage (kms)", "Daily Price", "Maintenance Cost", "Available"),    # Column names shown on top of displayed data
    EMPTY_MESSAGE = "No vehicles in existance.",                                                            # Message displayed when no data is found
    GENERATE_MODEL = lambda content: (                                                                      # Function used to generate strings of rows with the provided data
        f"{content[0]:<13} | "                                                                              # Formatted strings to take in content and add at least 13 blank spaces, regardless of string size
        f"{content[1]:<13} | "
        f"{content[2]:<13} | "
        f"{content[3]:<13} | "
        f"€{content[4]:<13} | "
        f"€{content[5]:<13} | "
        f"{'Yes' if content[6] else 'No':<13}"
    )
)

BOOKING=SimpleNamespace(                                                                # Variable with strings to be used in BookingInterface
    TITLE = "Booking Management"                                                        # Title of interface
)

RETURN=SimpleNamespace(                                                                 # Variable with strings to be used in ReturnInterface
    TITLES = ("Return Management", "Select a booked vehicle:"),                         # Title and subtitle of interface
    HEADERS = ("ID", "Brand", "Model", "Mileage", "Daily Price", "Maintenance Cost"),   # Column names shown on top of displayed data
    EMPTY_MESSAGE = "No booked vehicles found.",                                        # Message displayed when no data is found
    GENERATE_MODEL = lambda content: (                                                  # Function used to generate strings of rows with the provided data; data is segmented 
        f"{content[0]:<15} | "                                                          # Formatted strings to take in content and add at least 15 blank spaces, regardless of string size
        f"{content[1]:<15} | "
        f"{content[2]:<15} | "
        f"{content[3]:<15} | "
        f"€{content[4]:<15} | "
        f"€{content[5]:<15}"
    )
)

MAINTENANCE=SimpleNamespace(                                                        # Variable with strings to be used in MaintenanceInterface
    TITLES = ("Maintenance Management", "Vehicles Needing Maintenance"),            # Title and subtitle of interface
    HEADERS = ("ID", "Brand", "Model", "Current Mileage", "Maintenance Cost"),      # Column names shown on top of displayed data
    EMPTY_MESSAGE = "All vehicles are in good condition.",                          # Message displayed when no data is found
    GENERATE_MODEL = lambda content: (                                              # Function used to generate strings of rows with the provided data
        f"{content[0]:<10} | "                                                      # Formatted strings to take in content and add at least 10 blank spaces, regardless of string size
        f"{content[1]:<10} | "
        f"{content[2]:<10} | "
        f"{content[3]:<10} | "
        f"€{content[4]:<10}"
    )
)

LOGS=SimpleNamespace(                                                                                                                                   # Variable with strings to be used in LogsInterface
    TITLES = ("Logs Management", "Transaction Logs"),                                                                                                   # Title and subtitle of interface
    HEADERS = ("Transaction ID", "Vehicle ID", "Customer Name", "Rental Duration (days)", "Revenue (€)", "Additional Costs (€)", "Transaction Type"),   # Column names shown on top of displayed data
    EMPTY_MESSAGE = "No transaction logs found.",                                                                                                       # Message displayed when no data is found
    GENERATE_MODEL = lambda content: (                                                                                                                  # Function used to generate strings of rows with the provided data
        f"{content[0]:<15} | "                                                                                                                          # Formatted strings to take in content and add at least 15 blank spaces, regardless of string size
        f"{content[1]:<15} | "
        f"{content[5]:<15} | "
        f"{content[2]:<15} | "
        f"€{content[3]:<15} | "
        f"€{content[4]:<15} | "
        f"{content[6]:<15}"
    )
)

METRICS=SimpleNamespace(                                                                                                        # Variable with strings to be used in MetricsInterface
    TITLES = ("Metrics Management", "Financial Metrics"),                                                                       # Title and subtitle of interface
    HEADERS = ("Total Revenue (€)", "Total Operational Costs (€)", "Total Profit (€)", "Average Mileage (km/vehicle)"),         # Column names shown on top of displayed data
    EMPTY_MESSAGE = "No financial data available.",                                                                             # Message displayed when no data is found
    PDF_HEADERS=SimpleNamespace(                                                                                                # Column names used when displaying data in the PDFs
        VEHICLES = ("ID", "Brand", "Model", "Mileage", "Daily Price", "Maintenance Cost", "Available", "Maintenance Mileage"),  # Column names for the 'vehicles' table
        BOOKINGS = ("ID", "Vehicle ID", "Rental Days", "Estimated KM", "Estimated Cost", "Customer Name"),                      # Column names for the 'bookings' table
        LOGS = ("ID", "Vehicle ID", "Rental Duration", "Revenue", "Additional Costs", "Customer Name", "Transaction Type"),     # Column names for the 'logs' table
    )
)