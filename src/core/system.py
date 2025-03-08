# system.py
from src.database.setup import initialize_database
from datetime import datetime, timedelta

class CarsharingSystem:
    def __init__(self):
        self.conn, self.cursor = initialize_database()

    def add_vehicle(self, brand, model, mileage, daily_price, maintenance_cost):
        self.cursor.execute("""
            INSERT INTO vehicles (brand, model, current_mileage, daily_price, maintenance_cost, maintenance_mileage)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (brand, model, mileage, daily_price, maintenance_cost,mileage + 10000))
        self.conn.commit()

    def get_all_vehicles(self):
        self.cursor.execute("SELECT * FROM vehicles")
        return self.cursor.fetchall()
    
    def get_vehicles_requiring_maintenance(self):
        self.cursor.execute("SELECT id, brand, model, current_mileage, maintenance_mileage FROM vehicles WHERE current_mileage >= maintenance_mileage")
        return self.cursor.fetchall()
    
    def get_unavailable_vehicles(self):
        """Fetches all vehicles with available = 0."""
        self.cursor.execute("SELECT * FROM vehicles WHERE available = 0")
        return self.cursor.fetchall()

    def query_update_availability(self, vehicle_id, available: bool):
        self.cursor.execute("""
            UPDATE vehicles
            SET available = ?
            WHERE id = ?
        """, (1 if available else 0, vehicle_id))
        self.conn.commit()

    def query_booking(self, vehicle_id, rental_days, estimated_km):
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
    
    def query_return(self, vehicle_id, actual_km, late_days):
        # Check if the vehicle exists
        self.cursor.execute("SELECT * FROM vehicles WHERE id = ?", (vehicle_id,))
        vehicle = self.cursor.fetchone()
        
        if not vehicle:
            return None  # Vehicle doesn't exist

        # Check if the vehicle is currently booked
        self.cursor.execute("SELECT * FROM bookings WHERE vehicle_id = ?", (vehicle_id,))
        booking = self.cursor.fetchone()
        
        if not booking:
            return None  # Vehicle is not currently booked

        # Extract booking details
        rental_days = booking[2]  # Assuming column 2 is 'rental_days'
        estimated_km = booking[3]  # Assuming column 3 is 'estimated_km'
        estimated_cost = booking[4]  # Assuming column 4 is 'estimated_cost'

        # Cost calculation logic
        km_exceeded = max(0, actual_km - estimated_km)  # Extra km
        late_fee = late_days * 20  # Example: charge 20€ per late day
        total_cost = estimated_cost + (km_exceeded * 0.5) + late_fee  # 0.5€/extra km

        new_mileage = vehicle[3] + actual_km

        # Update database: Mark booking as returned and update vehicle availability
        self.cursor.execute("DELETE FROM bookings WHERE vehicle_id = ?", (vehicle_id,))
        self.cursor.execute("UPDATE vehicles SET current_mileage = ?, available = 1 WHERE id = ?", (new_mileage, vehicle_id,))

        # Commit changes
        self.conn.commit()
        return total_cost


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