from src.pages.interfaces.inventory_interface import InventoryInterface             # Import the interface for managing vehicle inventory
from src.pages.interfaces.booking_interface import BookingInterface                 # Import the interface for handling vehicle bookings
from src.pages.interfaces.return_interface import ReturnInterface                   # Import the interface for processing vehicle returns
from src.pages.interfaces.maintenance_interface import MaintenanceInterface         # Import the interface for managing vehicle maintenance
from src.pages.interfaces.logs_interface import LogsInterface                       # Import the interface for viewing transaction logs
from src.pages.interfaces.metrics_interface import MetricsInterface                 # Import the interface for viewing metrics and analytics

from types import SimpleNamespace                                                   # Import SimpleNamespace to create nested namespaces for organizing constants

SQL = SimpleNamespace(                  # Define a nested namespace for SQL-related constants
    OPERATION=SimpleNamespace(          # Define constants for SQL operations (SELECT, INSERT, UPDATE, DELETE)
        SELECT="SELECT",                # SQL SELECT operation string
        INSERT="INSERT",                # SQL INSERT operation string
        UPDATE="UPDATE",                # SQL UPDATE operation string
        DELETE="DELETE",                # SQL DELETE operation string
    ),
    TABLE=SimpleNamespace(              # Define constants for table names in the database
        VEHICLES="vehicles",            # Name string for the table storing vehicle information
        BOOKINGS="bookings",            # Name string for the table for storing booking information
        LOGS="logs"                     # Name string for the table for storing transaction logs
    ),
    FETCH=SimpleNamespace(              # Define constants for fetch operations (fetch one row or all rows)
        ONE="one",                      # Fetch a single row from the database
        ALL="all"                       # Fetch all rows from the database
    )
)

DB_NAME = "carsharing.db"               # Define the name of the SQLite database file

DATABASE_TABLE_STATEMENTS = (           # Define SQL statements for creating database tables (and their columns) if they don't already exist
    """
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            current_mileage INTEGER NOT NULL,
            daily_price REAL NOT NULL,
            maintenance_cost REAL NOT NULL,
            available INTEGER DEFAULT 1,
            maintenance_mileage INTEGER NOT NULL
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER NOT NULL,
            rental_days INTEGER NOT NULL,
            estimated_km INTEGER NOT NULL,
            estimated_cost REAL NOT NULL,
            customer_name TEXT NOT NULL,
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER NOT NULL,
            rental_duration INTEGER NOT NULL,
            revenue REAL NOT NULL,
            additional_costs REAL DEFAULT 0.0,
            customer_name TEXT NOT NULL,
            transaction_type TEXT NOT NULL,
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
        )
    """
)

INTERFACES_LIST = [                        # Define a list of interfaces for the application, mapping names to their corresponding classes
    InventoryInterface,                     # Interface for managing vehicle inventory
    BookingInterface,                       # Interface for handling vehicle bookings
    ReturnInterface,                        # Interface for handling vehicle returns
    MaintenanceInterface,                   # Interface for managing vehicle maintenance
    LogsInterface,                          # Interface for viewing transaction logs
    MetricsInterface,                       # Interface for viewing metrics and querying
]