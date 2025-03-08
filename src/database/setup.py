# database.py
import sqlite3

from src.misc.constants import DB_NAME

def initialize_database():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create the vehicles table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            current_mileage INTEGER NOT NULL,
            maintenance_mileage INTEGER NOT NULL,
            daily_price REAL NOT NULL,
            maintenance_cost REAL NOT NULL,
            available INTEGER DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER NOT NULL,
            rental_days INTEGER NOT NULL,
            estimated_km INTEGER NOT NULL,
            estimated_cost REAL NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
        )
    """)

    # Commit the changes and close the connection
    conn.commit()
    
    return conn, cursor