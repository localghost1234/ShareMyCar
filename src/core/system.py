# system.py
from src.core.database import Database

class System:
    def __init__(self):
        self.database = Database()

    def add_vehicle(self, brand, model, mileage, daily_price, maintenance_cost):
        self.database.execute_query("""
            INSERT INTO vehicles (brand, model, current_mileage, daily_price, maintenance_cost, maintenance_mileage)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (brand, model, mileage, daily_price, maintenance_cost, mileage + 10000))
        self.database.commit()

    def get_all_vehicles(self):
        self.database.execute_query("SELECT * FROM vehicles")
        return self.database.fetchall()
    
    def get_all_bookings(self):
        self.database.execute_query("SELECT * FROM bookings")
        return self.database.fetchall()
    
    def get_transaction_logs(self):
        self.database.execute_query("SELECT * FROM logs")
        return self.database.fetchall()
    
    def get_vehicles_requiring_maintenance(self):
        self.database.execute_query("""SELECT
                                    id,
                                    brand,
                                    model,
                                    current_mileage,
                                    maintenance_mileage
                                    FROM vehicles
                                    WHERE current_mileage >= maintenance_mileage""")
        return self.database.fetchall()
    
    def get_unavailable_vehicles(self):
        """Fetches all vehicles with available = 0."""
        self.database.execute_query("SELECT * FROM vehicles WHERE available = 0")
        return self.database.fetchall()
    
    def get_customer_name(self, vehicle_id):
        self.database.execute_query("SELECT customer_name FROM bookings WHERE vehicle_id = ?", (vehicle_id,))
        name = self.database.fetchone()
        return name[0] if name else "Unknown Customer"
    
    def get_financial_metrics(self):
        """Fetches and calculates financial metrics from the database."""
        self.database.execute_query("SELECT * FROM logs")
        is_there_log = self.database.fetchone()

        if not is_there_log:
            return ()
        
        # Get total revenue from logs
        self.database.execute_query("SELECT SUM(revenue) FROM logs")
        total_revenue = self.database.fetchone()[0] or 0

        # Get total maintenance costs from vehicles
        self.database.execute_query("SELECT SUM(maintenance_cost) FROM vehicles")
        total_maintenance_cost = self.database.fetchone()[0] or 0

        # Get total additional costs from logs (e.g., extra fees, cleaning costs)
        self.database.execute_query("SELECT SUM(additional_costs) FROM logs")
        total_additional_costs = self.database.fetchone()[0] or 0

        # Calculate total operational costs
        total_operational_costs = total_maintenance_cost + total_additional_costs

        # Calculate total profit
        total_profit = total_revenue - total_operational_costs

        # Get average mileage per vehicle
        self.database.execute_query("SELECT AVG(current_mileage) FROM vehicles")
        avg_mileage = self.database.fetchone()[0] or 0

        metrics = (
            total_revenue,
            total_operational_costs,
            total_profit,
            avg_mileage,
        )

        return metrics

    def query_update_availability(self, vehicle_id, available: bool):
        self.database.execute_query("""
            UPDATE vehicles
            SET available = ?
            WHERE id = ?
        """, (1 if available else 0, vehicle_id))
        self.database.commit()

    def query_booking(self, vehicle_id, rental_days, estimated_km, customer_name):
        """Books a vehicle, calculates cost, and updates the database."""
        # Check if the vehicle is available
        self.database.execute_query("SELECT daily_price, maintenance_cost, available FROM vehicles WHERE id = ?", (vehicle_id,))
        vehicle = self.database.fetchone()

        if not vehicle:
            return None  # Vehicle does not exist

        daily_price, maintenance_cost, available = vehicle

        if available == 0:
            return None  # Vehicle is already booked

        # Calculate estimated cost
        additional_cost = maintenance_cost * estimated_km
        total_estimated_cost = (daily_price * rental_days) + additional_cost

        # Insert booking record
        self.database.execute_query("""
            INSERT INTO bookings (vehicle_id, rental_days, estimated_km, estimated_cost, customer_name)
            VALUES (?, ?, ?, ?, ?)
        """, (vehicle_id, rental_days, estimated_km, total_estimated_cost, customer_name))

        # Insert booking record
        self.database.execute_query("""
            INSERT INTO logs (vehicle_id, rental_duration, revenue, additional_costs, customer_name, transaction_type)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (vehicle_id, rental_days, total_estimated_cost, additional_cost, customer_name, "booking"))

        # Mark vehicle as unavailable
        self.database.execute_query("UPDATE vehicles SET available = 0 WHERE id = ?", (vehicle_id,))

        self.database.commit()
        return total_estimated_cost
    
    def query_return(self, vehicle_id, actual_km, late_days, customer_name):
        # Check if the vehicle exists
        self.database.execute_query("SELECT * FROM vehicles WHERE id = ?", (vehicle_id,))
        vehicle = self.database.fetchone()
        
        if not vehicle:
            return None  # Vehicle doesn't exist

        # Check if the vehicle is currently booked
        self.database.execute_query("SELECT * FROM bookings WHERE vehicle_id = ?", (vehicle_id,))
        booking = self.database.fetchone()
        
        if not booking:
            return None  # Vehicle is not currently booked

        # Extract booking details
        rental_days = booking[2]  # Assuming column 2 is 'rental_days'
        estimated_km = booking[3]  # Assuming column 3 is 'estimated_km'
        estimated_cost = booking[4]  # Assuming column 4 is 'estimated_cost'

        # Cost calculation logic
        cleaning_fees = 20
        km_exceeded = max(0, actual_km - estimated_km)  # Extra km
        lateness_fee = late_days * 10  # charge 10€ per late day
        exceeded_mileage_fee = km_exceeded * 0.5 # 0.5€ per extra km
        additional_costs = exceeded_mileage_fee + lateness_fee + cleaning_fees
        total_revenue = estimated_cost + additional_costs

        new_mileage = vehicle[3] + actual_km

        # Update database: Mark booking as returned and update vehicle availability
        self.database.execute_query("DELETE FROM bookings WHERE vehicle_id = ?", (vehicle_id,))
        self.database.execute_query("UPDATE vehicles SET current_mileage = ?, available = 1 WHERE id = ?", (new_mileage, vehicle_id,))

        self.database.execute_query("""
            INSERT INTO logs (vehicle_id, rental_duration, revenue, additional_costs, customer_name, transaction_type)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (vehicle_id, rental_days, total_revenue, additional_costs, customer_name, "return"))

        # Commit changes
        self.database.commit()
        return total_revenue


    def close(self):
        self.database.close()