from src.pages.interfaces.inventory_interface import InventoryInterface
from src.pages.interfaces.booking_interface import BookingInterface
from src.pages.interfaces.return_interface import ReturnInterface
from src.pages.interfaces.maintenance_interface import MaintenanceInterface
from src.pages.interfaces.logs_interface import LogsInterface
from src.pages.interfaces.metrics_interface import MetricsInterface

DB_NAME = "carsharing.db"

INTERFACES_LIST = [
            ("Inventory", InventoryInterface),
            ("Booking", BookingInterface),
            ("Return", ReturnInterface),
            ("Maintenance", MaintenanceInterface),
            ("Logs", LogsInterface),
            ("Metrics", MetricsInterface),
        ]
