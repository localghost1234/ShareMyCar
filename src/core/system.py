# core_logic.py
import sqlite3
from datetime import datetime, timedelta

class CarsharingSystem:
    def __init__(self):
        self.conn = sqlite3.connect("carsharing.db")
        self.cursor = self.conn.cursor()

    def add_vehicle(self, brand, model, mileage, daily_price, maintenance_cost):
        self.cursor.execute("""
            INSERT INTO vehicles (brand, model, mileage, daily_price, maintenance_cost)
            VALUES (?, ?, ?, ?, ?)
        """, (brand, model, mileage, daily_price, maintenance_cost))
        self.conn.commit()

    def get_vehicles(self):
        self.cursor.execute("SELECT * FROM vehicles")
        return self.cursor.fetchall()

    def update_availability(self, vehicle_id, available):
        self.cursor.execute("""
            UPDATE vehicles
            SET available = ?
            WHERE id = ?
        """, (available, vehicle_id))
        self.conn.commit()

    def book_vehicle(self, vehicle_id, rental_days, estimated_km):
        """Books a vehicle, calculates cost, and updates the database."""
        # Check if the vehicle is available
        self.cursor.execute("SELECT daily_price, maintenance_cost, available FROM vehicles WHERE id = ?", (vehicle_id,))
        vehicle = self.cursor.fetchone()

        if not vehicle:
            return None  # Vehicle does not exist

        daily_price, maintenance_cost, available = vehicle

        if available == 0:
            return None  # Vehicle is already booked

        # Calculate estimated cost
        estimated_cost = (daily_price * rental_days) + (maintenance_cost * estimated_km)

        # Calculate rental period
        start_date = datetime.now()
        end_date = start_date + timedelta(days=rental_days)

        # Insert booking record
        self.cursor.execute("""
            INSERT INTO bookings (vehicle_id, rental_days, estimated_km, estimated_cost, start_date, end_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (vehicle_id, rental_days, estimated_km, estimated_cost, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))

        # Mark vehicle as unavailable
        self.cursor.execute("UPDATE vehicles SET available = 0 WHERE id = ?", (vehicle_id,))

        self.conn.commit()
        return estimated_cost

    def close(self):
        self.conn.close()