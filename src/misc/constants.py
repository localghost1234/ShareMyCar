from src.pages.interfaces.inventory_interface import InventoryInterface
from src.pages.interfaces.booking_interface import BookingInterface
from src.pages.interfaces.return_interface import ReturnInterface
from src.pages.interfaces.maintenance_interface import MaintenanceInterface
from src.pages.interfaces.logs_interface import LogsInterface
from src.pages.interfaces.metrics_interface import MetricsInterface

DB_NAME = "carsharing.db"

DATABASE_TABLES_STATEMENTS = (
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

INTERFACES_LIST = (
            ("Inventory", InventoryInterface),
            ("Booking", BookingInterface),
            ("Return", ReturnInterface),
            ("Maintenance", MaintenanceInterface),
            ("Logs", LogsInterface),
            ("Metrics", MetricsInterface),
        )