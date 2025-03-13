# system.py
from src.core.database import Database
from src.misc.constants import SQL

class System:
    def __init__(self):
        self.database = Database()

    def add_vehicle(self, brand, model, mileage, daily_price, maintenance_cost):
        self.database.execute_query(
            operation=SQL.OPERATION.INSERT,
            table=SQL.TABLE.VEHICLES,
            columns=["brand", "model", "current_mileage", "daily_price", "maintenance_cost", "maintenance_mileage"],
            values=(brand, model, mileage, daily_price, maintenance_cost, mileage + 10000)
        )
        self.database.commit()

    def get_all_vehicles(self):
        return self.database.execute_query(
            operation=SQL.OPERATION.SELECT,
            table=SQL.TABLE.VEHICLES,
            fetch=SQL.FETCH.ALL
        )

    def get_all_bookings(self):
        return self.database.execute_query(
            operation=SQL.OPERATION.SELECT,
            table=SQL.TABLE.BOOKINGS,
            fetch=SQL.FETCH.ALL
        )

    def get_transaction_logs(self):
        return self.database.execute_query(
            operation=SQL.OPERATION.SELECT,
            table=SQL.TABLE.LOGS,
            fetch=SQL.FETCH.ALL
        )

    def get_vehicles_requiring_maintenance(self):
        return self.database.execute_query(
            operation=SQL.OPERATION.SELECT,
            table=SQL.TABLE.VEHICLES,
            columns=["id", "brand", "model", "current_mileage", "maintenance_mileage"],
            where="current_mileage >= maintenance_mileage",
            fetch=SQL.FETCH.ALL
        )

    def get_unavailable_vehicles(self):
        return self.database.execute_query(
            operation=SQL.OPERATION.SELECT,
            table=SQL.TABLE.VEHICLES,
            where="available = 0",
            fetch=SQL.FETCH.ALL
        )

    def get_customer_name(self, vehicle_id):
        result = self.database.execute_query(
            operation=SQL.OPERATION.SELECT,
            table=SQL.TABLE.BOOKINGS,
            columns=["customer_name"],
            where=f"vehicle_id = {vehicle_id}",
            fetch=SQL.FETCH.ONE
        )
        return result[0] if result else "Unknown Customer"

    def get_financial_metrics(self):
        """Fetches and calculates financial metrics from the database."""
        # Check if there are any logs
        logs_exist = self.database.execute_query(
            operation=SQL.OPERATION.SELECT,
            table=SQL.TABLE.LOGS,
            fetch=SQL.FETCH.ONE
        )
        if not logs_exist:
            return ()

        # Get total revenue from logs
        total_revenue = self.database.execute_query(
            operation=SQL.OPERATION.SELECT,
            table=SQL.TABLE.LOGS,
            columns=["SUM(revenue)"],
            fetch=SQL.FETCH.ONE
        )[0] or 0

        # Get total maintenance costs from vehicles
        total_maintenance_cost = self.database.execute_query(
            operation=SQL.OPERATION.SELECT,
            table=SQL.TABLE.VEHICLES,
            columns=["SUM(maintenance_cost)"],
            fetch=SQL.FETCH.ONE
        )[0] or 0

        # Get total additional costs from logs
        total_additional_costs = self.database.execute_query(
            operation=SQL.OPERATION.SELECT,
            table=SQL.TABLE.LOGS,
            columns=["SUM(additional_costs)"],
            fetch=SQL.FETCH.ONE
        )[0] or 0

        # Calculate total operational costs
        total_operational_costs = total_maintenance_cost + total_additional_costs

        # Calculate total profit
        total_profit = total_revenue - total_operational_costs

        # Get average mileage per vehicle
        avg_mileage = self.database.execute_query(
            operation=SQL.OPERATION.SELECT,
            table=SQL.TABLE.VEHICLES,
            columns=["AVG(current_mileage)"],
            fetch=SQL.FETCH.ONE
        )[0] or 0

        metrics = (
            total_revenue,
            total_operational_costs,
            total_profit,
            avg_mileage,
        )

        return metrics

    def query_update_availability(self, vehicle_id, available: bool):
        self.database.execute_query(
            operation=SQL.OPERATION.UPDATE,
            table=SQL.TABLE.VEHICLES,
            columns=["available"],
            values=(1 if available else 0,),
            where=f"id = {vehicle_id}"
        )
        self.database.commit()

    def query_booking(self, vehicle_id, rental_days, estimated_km, customer_name):
        """Books a vehicle, calculates cost, and updates the database."""
        # Check if the vehicle is available
        vehicle = self.database.execute_query(
            operation=SQL.OPERATION.SELECT,
            table=SQL.TABLE.VEHICLES,
            columns=["daily_price", "maintenance_cost", "available"],
            where=f"id = {vehicle_id}",
            fetch=SQL.FETCH.ONE
        )

        if not vehicle:
            return None  # Vehicle does not exist

        daily_price, maintenance_cost, available = vehicle

        if available == 0:
            return None  # Vehicle is already booked

        # Calculate estimated cost
        additional_cost = maintenance_cost * estimated_km
        total_estimated_cost = (daily_price * rental_days) + additional_cost

        # Insert booking record
        self.database.execute_query(
            operation=SQL.OPERATION.INSERT,
            table=SQL.TABLE.BOOKINGS,
            columns=["vehicle_id", "rental_days", "estimated_km", "estimated_cost", "customer_name"],
            values=(vehicle_id, rental_days, estimated_km, total_estimated_cost, customer_name)
        )

        # Insert log record
        self.database.execute_query(
            operation=SQL.OPERATION.INSERT,
            table=SQL.TABLE.LOGS,
            columns=["vehicle_id", "rental_duration", "revenue", "additional_costs", "customer_name", "transaction_type"],
            values=(vehicle_id, rental_days, total_estimated_cost, additional_cost, customer_name, "booking")
        )

        # Mark vehicle as unavailable
        self.database.execute_query(
            operation=SQL.OPERATION.UPDATE,
            table=SQL.TABLE.VEHICLES,
            columns=["available"],
            values=(0,),
            where=f"id = {vehicle_id}"
        )

        self.database.commit()
        return total_estimated_cost

    def query_return(self, vehicle_id, actual_km, late_days, customer_name):
        # Check if the vehicle exists
        vehicle = self.database.execute_query(
            operation=SQL.OPERATION.SELECT,
            table=SQL.TABLE.VEHICLES,
            where=f"id = {vehicle_id}",
            fetch=SQL.FETCH.ONE
        )

        if not vehicle:
            return None  # Vehicle doesn't exist

        # Check if the vehicle is currently booked
        booking = self.database.execute_query(
            operation=SQL.OPERATION.SELECT,
            table=SQL.TABLE.BOOKINGS,
            where=f"vehicle_id = {vehicle_id}",
            fetch=SQL.FETCH.ONE
        )

        if not booking:
            return None  # Vehicle is not currently booked

        # Extract booking details
        rental_days = booking[2]  # Assuming column 2 is 'rental_days'
        estimated_km = booking[3]  # Assuming column 3 is 'estimated_km'
        estimated_cost = booking[4]  # Assuming column 4 is 'estimated_cost'

        # Cost calculation logic
        cleaning_fees = 20
        km_exceeded = max(0, actual_km - estimated_km)  # Extra km
        lateness_fee = late_days * 10  # Charge 10€ per late day
        exceeded_mileage_fee = km_exceeded * 0.5  # 0.5€ per extra km
        additional_costs = exceeded_mileage_fee + lateness_fee + cleaning_fees
        total_revenue = estimated_cost + additional_costs

        new_mileage = vehicle[3] + actual_km

        # Update database: Mark booking as returned and update vehicle availability
        self.database.execute_query(
            operation=SQL.OPERATION.DELETE,
            table=SQL.TABLE.BOOKINGS,
            where=f"vehicle_id = {vehicle_id}"
        )

        self.database.execute_query(
            operation=SQL.OPERATION.UPDATE,
            table=SQL.TABLE.VEHICLES,
            columns=["current_mileage", "available"],
            values=(new_mileage, 1),
            where=f"id = {vehicle_id}"
        )

        # Insert log record
        self.database.execute_query(
            operation=SQL.OPERATION.INSERT,
            table=SQL.TABLE.LOGS,
            columns=["vehicle_id", "rental_duration", "revenue", "additional_costs", "customer_name", "transaction_type"],
            values=(vehicle_id, rental_days, total_revenue, additional_costs, customer_name, "return")
        )

        # Commit changes
        self.database.commit()
        return total_revenue

    def close(self):
        self.database.close()