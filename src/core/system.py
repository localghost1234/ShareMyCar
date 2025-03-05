# core_logic.py
import sqlite3

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

    def close(self):
        self.conn.close()