from src.pages.interfaces.home_interface import HomeInterface                       # Import the interface for home
from src.pages.interfaces.inventory_interface import InventoryInterface             # Import the interface for managing vehicle inventory
from src.pages.interfaces.booking_interface import BookingInterface                 # Import the interface for handling vehicle bookings
from src.pages.interfaces.return_interface import ReturnInterface                   # Import the interface for processing vehicle returns
from src.pages.interfaces.maintenance_interface import MaintenanceInterface         # Import the interface for managing vehicle maintenance
from src.pages.interfaces.logs_interface import LogsInterface                       # Import the interface for viewing transaction logs
from src.pages.interfaces.metrics_interface import MetricsInterface                 # Import the interface for viewing metrics and analytics

INTERFACES_CLASS = (                        # Define a list of interfaces for the application, mapping names to their corresponding classes
    HomeInterface,
    InventoryInterface,                     # Interface for managing vehicle inventory
    BookingInterface,                       # Interface for handling vehicle bookings
    ReturnInterface,                        # Interface for handling vehicle returns
    MaintenanceInterface,                   # Interface for managing vehicle maintenance
    LogsInterface,                          # Interface for viewing transaction logs
    MetricsInterface,                       # Interface for viewing metrics and querying
)

DB_NAME = "carsharing_database.json"               # Define the name of the SQLite database file

"""
DATABASE_TABLE_STATEMENTS = (           # Define SQL statements for creating database tables (and their columns) if they don't already exist
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            current_mileage INTEGER NOT NULL,
            daily_price REAL NOT NULL,
            maintenance_cost REAL NOT NULL,
            available INTEGER DEFAULT 1,
            maintenance_mileage INTEGER NOT NULL
        ),
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER NOT NULL,
            rental_duration INTEGER NOT NULL,
            estimated_km INTEGER NOT NULL,
            estimated_cost REAL NOT NULL,
            customer_name TEXT NOT NULL,
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
        ),
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
)
"""