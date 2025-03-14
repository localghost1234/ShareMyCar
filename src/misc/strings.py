from types import SimpleNamespace

INVENTORY=SimpleNamespace(
    TITLES = ("Inventory Management", "All existing vehicles"),
    HEADERS = ("ID", "Brand", "Model", "Mileage (kms)", "Daily Price", "Maintenance Cost", "Available"),
    EMPTY_MESSAGE = "No vehicles available.",
    GENERATE_MODEL = lambda content: (
        f"{content[0]:<13} | "
        f"{content[1]:<13} | "
        f"{content[2]:<13} | "
        f"{content[3]:<13} | "
        f"€{content[4]:<13} | "
        f"€{content[5]:<13} | "
        f"{'Yes' if content[6] else 'No':<13}"
    )
)

BOOKING=SimpleNamespace(
    TITLE = "Booking Management"
)

RETURN=SimpleNamespace(
    TITLES = ("Return Management", "Select a booked vehicle:"),
    HEADERS = ("ID", "Brand", "Model", "Mileage", "Daily Price", "Maintenance Cost"),
    EMPTY_MESSAGE = "No booked vehicles found.",
    GENERATE_MODEL = lambda content: (
        f"{content[0]:<15} | "
        f"{content[1]:<15} | "
        f"{content[2]:<15} | "
        f"{content[3]:<15} | "
        f"€{content[4]:<15} | "
        f"€{content[5]:<15}"
    )
)

MAINTENANCE=SimpleNamespace(
    TITLES = ("Maintenance Management", "Vehicles Needing Maintenance"),
    HEADERS = ("ID", "Brand", "Model", "Current Mileage", "Maintenance Cost"),
    EMPTY_MESSAGE = "All vehicles are in good condition.",
    GENERATE_MODEL = lambda content: (
        f"{content[0]:<10} | "
        f"{content[1]:<10} | "
        f"{content[2]:<10} | "
        f"{content[3]:<10} | "
        f"€{content[4]:<10}"
    )
)

LOGS=SimpleNamespace(
    TITLES = ("Logs Management", "Transaction Logs"),
    HEADERS = ("Transaction ID", "Vehicle ID", "Customer Name", "Rental Duration (days)", "Revenue (€)", "Additional Costs (€)", "Transaction Type"),
    EMPTY_MESSAGE = "No transaction logs found.",
    GENERATE_MODEL = lambda content: (
        f"{content[0]:<15} | "
        f"{content[1]:<15} | "
        f"{content[5]:<15} | "
        f"{content[2]:<15} | "
        f"€{content[3]:<15} | "
        f"€{content[4]:<15} | "
        f"{content[6]:<15}"
    )
)

METRICS=SimpleNamespace(
    TITLES = ("Metrics Management", "Financial Metrics"),
    HEADERS = ("Total Revenue (€)", "Total Costs (€)", "Total Profit (€)", "Avg Mileage (km/vehicle)"),
    EMPTY_MESSAGE = "No financial data available.",
    PDF_HEADERS=SimpleNamespace(
        VEHICLES = ("ID", "Brand", "Model", "Mileage", "Daily Price", "Maintenance Cost", "Available", "Maintenance Mileage"),
        BOOKINGS = ("ID", "Vehicle ID", "Rental Days", "Estimated KM", "Estimated Cost", "Customer Name"),
        LOGS = ("ID", "Vehicle ID", "Rental Duration", "Revenue", "Additional Costs", "Customer Name", "Transaction Type"),
    )
)