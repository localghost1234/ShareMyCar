from src.core.database import Database  # Import the Database class
from src.misc.constants import SQL  # Import SQL constants

class System:
    """Handles vehicle rentals, transactions, and database operations."""
    def __init__(self):
        self.database = Database()  # Initialize database connection

    def add_vehicle(self, brand, model, mileage, daily_price, maintenance_cost):
        """Adds a new vehicle to the database."""
        self.database.execute_query(
            operation=SQL.OPERATION.INSERT,  # SQL insert operation
            table=SQL.TABLE.VEHICLES,  # Target table
            columns=["brand", "model", "current_mileage", "daily_price", "maintenance_cost", "maintenance_mileage"],  # Columns to insert
            values=(brand, model, mileage, daily_price, maintenance_cost, mileage + 10000)  # Values to insert
        )
        self.database.commit()  # this command tells the database to 'write' our data into the DB

    def get_all_vehicles(self):
        """Retrieves all vehicles from the database."""
        return self.database.execute_query(
            operation=SQL.OPERATION.SELECT,  # SQL select operation
            table=SQL.TABLE.VEHICLES,  # Target table
            fetch=SQL.FETCH.ALL  # Fetch all records
        )

    def get_all_bookings(self):
        """Retrieves all bookings from the database."""
        return self.database.execute_query(
            operation=SQL.OPERATION.SELECT,  # SQL select operation
            table=SQL.TABLE.BOOKINGS,  # Target table
            fetch=SQL.FETCH.ALL  # Fetch all records
        )

    def get_transaction_logs(self):
        """Retrieves all transaction logs from the database."""
        return self.database.execute_query(
            operation=SQL.OPERATION.SELECT,  # SQL select operation
            table=SQL.TABLE.LOGS,  # Target table
            fetch=SQL.FETCH.ALL  # Fetch all records
        )

    def get_vehicles_requiring_maintenance(self):
        """Retrieves vehicles that require maintenance."""
        return self.database.execute_query(
            operation=SQL.OPERATION.SELECT,  # SQL select operation
            table=SQL.TABLE.VEHICLES,  # Target table
            columns=["id", "brand", "model", "current_mileage", "maintenance_mileage"],  # Relevant columns
            where="current_mileage >= maintenance_mileage",  # Condition for maintenance
            fetch=SQL.FETCH.ALL  # Fetch all matching records
        )

    def get_unavailable_vehicles(self):
        """Retrieves vehicles that are currently unavailable."""
        return self.database.execute_query(
            operation=SQL.OPERATION.SELECT,  # SQL select operation
            table=SQL.TABLE.VEHICLES,  # Target table
            where="available = 0",  # Condition for unavailability
            fetch=SQL.FETCH.ALL  # Fetch all matching records
        )

    def get_customer_name(self, vehicle_id):
        """Retrieves the name of the customer who booked a specific vehicle."""
        result = self.database.execute_query(
            operation=SQL.OPERATION.SELECT,  # SQL select operation
            table=SQL.TABLE.BOOKINGS,  # Target table
            columns=["customer_name"],  # Retrieve customer name
            where=f"vehicle_id = {vehicle_id}",  # Condition for specific vehicle
            fetch=SQL.FETCH.ONE  # Fetch a single record
        )
        return result[0] if result else "Unknown Customer"  # Return customer name or default value

    def get_financial_metrics(self):
        """Fetches and calculates financial metrics from the database."""
        logs_exist = self.database.execute_query(
            operation=SQL.OPERATION.SELECT,  # SQL select operation
            table=SQL.TABLE.LOGS,  # Target table
            fetch=SQL.FETCH.ONE,  # Fetch a single record
            where="transaction_type = 'return'"  # Check if any return transactions exist
        )
        if not logs_exist:
            return ()  # Return empty tuple if no logs exist

        total_revenue = self.database.execute_query(
            operation=SQL.OPERATION.SELECT,  # SQL select operation
            table=SQL.TABLE.LOGS,  # Target table
            columns=["SUM(revenue)"],  # Sum total revenue
            fetch=SQL.FETCH.ONE,
            where="transaction_type = 'return'"  # Filter by return transactions
        )[0] or 0  # Default to 0 if no data

        total_maintenance_cost = self.database.execute_query(
            operation=SQL.OPERATION.SELECT,  # SQL select operation
            table=SQL.TABLE.VEHICLES,  # Target table
            columns=["SUM(maintenance_cost)"],  # Sum maintenance costs
            fetch=SQL.FETCH.ONE,
        )[0] or 0  # Default to 0 if no data

        total_additional_costs = self.database.execute_query(
            operation=SQL.OPERATION.SELECT,  # SQL select operation
            table=SQL.TABLE.LOGS,  # Target table
            columns=["SUM(additional_costs)"],  # Sum additional costs
            fetch=SQL.FETCH.ONE,
            where="transaction_type = 'return'"  # Filter by return transactions
        )[0] or 0  # Default to 0 if no data

        total_operational_costs = total_maintenance_cost + total_additional_costs  # Calculate total costs
        total_profit = total_revenue - total_operational_costs  # Calculate profit

        avg_mileage = self.database.execute_query(
            operation=SQL.OPERATION.SELECT,  # SQL select operation
            table=SQL.TABLE.VEHICLES,  # Target table
            columns=["AVG(current_mileage)"],  # Calculate average mileage
            fetch=SQL.FETCH.ONE,
        )[0] or 0  # Default to 0 if no data

        return total_revenue, total_operational_costs, total_profit, avg_mileage  # Return metrics

    def query_update_availability(self, vehicle_id, available: bool):
        """Updates the availability status of a vehicle."""
        self.database.execute_query(
            operation=SQL.OPERATION.UPDATE,  # SQL update operation
            table=SQL.TABLE.VEHICLES,  # Target table
            columns=["available"],  # Column to update
            values=(1 if available else 0,),  # Set availability status
            where=f"id = {vehicle_id}"  # Target specific vehicle
        )
        self.database.commit()  # Commit transaction

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
        """Closes the database connection."""
        self.database.close()  # Sends a 'close' signal to the DB object
