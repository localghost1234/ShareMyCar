# database.py
import sqlite3

from src.misc.constants import DB_NAME

STATEMENT_CREATE_VEHICLES_TABLE = """
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
        """

STATEMENT_CREATE_BOOKINGS_TABLE = """
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehicle_id INTEGER NOT NULL,
                rental_days INTEGER NOT NULL,
                estimated_km INTEGER NOT NULL,
                estimated_cost REAL NOT NULL,
                customer_name TEXT NOT NULL,
                FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
            )
        """

STATEMENT_CREATE_LOGS_TABLE = """
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

class Database():
    def __init__(self):
        # Connect to the SQLite database (or create it if it doesn't exist)
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()

        # Create the vehicles table
        self.cursor.execute(STATEMENT_CREATE_VEHICLES_TABLE)
        self.cursor.execute(STATEMENT_CREATE_BOOKINGS_TABLE)
        self.cursor.execute(STATEMENT_CREATE_LOGS_TABLE)

        # Commit the changes and close the connection
        self.conn.commit()

    def execute_query(self, statement, params=()):
        self.cursor.execute(statement, params)

    def commit(self):
        self.conn.commit()

    def close(self):
        try:
            # Commit any pending transactions
            self.conn.commit()
        except Exception as e:
            print(f"Error committing transactions: \n{e}")

        try:
            self.cursor.close()
        except Exception as e:
            print(f"Error closing the cursor: \n{e}")
        
        try:
            # Close the database connection
            self.conn.close()
        except Exception as e:
            print(f"Error closing the database connection: \n{e}")