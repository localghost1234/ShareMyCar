from src.core.database import Database      # Import the Database class
from src.misc.constants import SQL          # Import SQL strings

class System:
    """Handles direct communication with database and defines its several use cases.
    
    Attributes:
        database (Database): The database connection instance.
    """
    def __init__(self):
        """Initialize the System with a database connection."""
        self.database = Database()

    def add_vehicle(self, brand, model, mileage, daily_price, maintenance_cost):
        """Adds a new vehicle to the database.
        
        Args:
            brand (str): Vehicle brand name
            model (str): Vehicle model name
            mileage (int): Current vehicle mileage
            daily_price (float): Daily rental price
            maintenance_cost (float): Cost per km for maintenance
        """
        self.database.execute_query(
            operation=SQL.OPERATION.INSERT,                                                                             # Indicates an SQL INSERT operation
            table=SQL.TABLE.VEHICLES,                                                                                   # Target table
            columns=["brand", "model", "current_mileage", "daily_price", "maintenance_cost", "maintenance_mileage"],    # Columns to insert
            values=[brand, model, mileage, daily_price, maintenance_cost, mileage + 10000],                             # Values to insert
        )
        self.database.commit()                                                                                          # This command tells the database to 'write' our new information into the DB

    def get_all_vehicles(self):
        """Returns a list of all the vehicles from the database.
        
        Returns:
            list: All vehicle records from the database
        """
        return self.database.execute_query(
            operation=SQL.OPERATION.SELECT,                 # Indicates an SQL SELECT operation
            table=SQL.TABLE.VEHICLES,                       # Target table
            fetch=SQL.FETCH.ALL,                            # Fetch all records
        )

    def get_all_bookings(self):
        """Returns a list of all the bookings from the database.
        
        Returns:
            list: All booking records from the database
        """
        return self.database.execute_query(
            operation=SQL.OPERATION.SELECT,                 # Indicates an SQL SELECT operation
            table=SQL.TABLE.BOOKINGS,                       # Target table
            fetch=SQL.FETCH.ALL,                            # Fetch all records
        )

    def get_all_logs(self):
        """Returns a list of all the transactions done with clients.
        
        Returns:
            list: All transaction log records from the database
        """
        return self.database.execute_query(
            operation=SQL.OPERATION.SELECT,                 # Indicates an SQL SELECT operation
            table=SQL.TABLE.LOGS,                           # Target table
            fetch=SQL.FETCH.ALL,                            # Fetch all records
        )

    def get_vehicles_requiring_maintenance(self):
        """Returns a list of vehicles which have surpassed their maintenance mileage.
        
        Returns:
            list: Vehicles requiring maintenance, with id, brand, model, current_mileage and maintenance_cost
        """
        return self.database.execute_query(
            operation=SQL.OPERATION.SELECT,                                                 # Indicates an SQL SELECT operation
            table=SQL.TABLE.VEHICLES,                                                       # Target table
            columns=["id", "brand", "model", "current_mileage", "maintenance_cost"],     # Relevant columns
            where="current_mileage >= maintenance_mileage",                                 # Condition to give maintenance
            fetch=SQL.FETCH.ALL,                                                            # Fetch all records
        )

    def get_unavailable_vehicles(self):
        """Returns a list of currently booked vehicles.
        
        Returns:
            list: All currently unavailable vehicles
        """
        return self.database.execute_query(
            operation=SQL.OPERATION.SELECT,                     # Indicates an SQL SELECT operation
            table=SQL.TABLE.VEHICLES,                           # Target table
            where="available = 0",                              # Adds a condition in which the vehicle is unavailable
            fetch=SQL.FETCH.ALL,                                # Fetch all records
        )
    
    def get_table_column(self, table_name, column_name):
        """Returns a list with all the database elements with the column label in a specified table.
        
        Args:
            table_name (str): Name of the table to query
            column_name (str): Name of the column to retrieve
            
        Returns:
            list: All values from the specified column in the specified table
        """
        return self.database.execute_query(
                    operation=SQL.OPERATION.SELECT,         # Indicates an SQL SELECT operation
                    table=table_name,                       # Target table
                    columns=[column_name],                  # Target column of the info
                    fetch=SQL.FETCH.ALL,                    # Fetch all records
                )

    def get_customer_name(self, vehicle_id):
        """Returns a string with the name of the customer who booked a specific vehicle. If not found, returns 'Unknown Customer'.
        
        Args:
            vehicle_id (int): ID of the vehicle to look up
            
        Returns:
            str: Customer name or 'Unknown Customer' if not found
        """
        result = self.database.execute_query(
            operation=SQL.OPERATION.SELECT,                     # Indicates an SQL SELECT operation
            table=SQL.TABLE.BOOKINGS,                           # Target table
            columns=["customer_name"],                          # Retrieve customer's name
            where=f"vehicle_id = {vehicle_id}",                 # Looks for a vehicle that matches the ID
            fetch=SQL.FETCH.ONE,                                # Fetch a single record
        )
        
        return result[0] if result else "Unknown Customer"      # Return customer name or a default value if nothing is found

    def get_financial_metrics(self):
        """Calculates and returns financial metrics.
        
        Returns a tuple with the calculated financial metrics:
            - Total revenue
            - Total operational costs
            - Total profit (revenue - costs)
            - Average mileage per vehicle
            
        Returns:
            tuple: (total_revenue, total_operational_costs, total_profit, average_vehicle_mileage)
            or empty tuple if no logs exist
        """
        logs_exist = self.database.execute_query(               # Requests database for a log data
            operation=SQL.OPERATION.SELECT,                     # Indicates an SQL SELECT operation
            table=SQL.TABLE.LOGS,                               # Target table
            fetch=SQL.FETCH.ONE,                                # Fetch a single record
            where="transaction_type = 'return'",                # Check only for 'return' type, because real earnings come from those only
        )

        if not logs_exist:                                      # Checks if there are any logs
            return ()                                           # Returns empty tuple if no logs exist
        
        total_revenue, total_additional_costs = self.database.execute_query(    # Obtains the aggregation of 'revenue' and 'additional_costs' from all the 'return' transaction logs
            operation=SQL.OPERATION.SELECT,                                     # Indicates an SQL SELECT operation
            table=SQL.TABLE.LOGS,                                               # Target table
            columns=["SUM(revenue)", "SUM(additional_costs)"],                  # Sum total revenue
            fetch=SQL.FETCH.ONE,                                                # Fetch a single record
            where="transaction_type = 'return'",                                # Check only for 'return' type, because real earnings come from those only
        ) or (0, 0)                                                             # Default to 0 for both if no data is available

        total_maintenance_cost, average_vehicle_mileage = self.database.execute_query(          # Obtains the aggregation of maintenance cost and average vehicle mileage of all existing vehicles
            operation=SQL.OPERATION.SELECT,                                                     # Indicates an SQL SELECT operation
            table=SQL.TABLE.VEHICLES,                                                           # Target table
            columns=["SUM(maintenance_cost)", "AVG(current_mileage)"],                          # Sum maintenance costs
            fetch=SQL.FETCH.ONE,                                                                # Fetch a single record
        ) or (0, 0)                                                                             # Default to 0 for both if no data is available

        total_operational_costs = total_maintenance_cost + total_additional_costs               # Calculate total costs
        total_profit = total_revenue - total_operational_costs                                  # Calculate profit

        return total_revenue, total_operational_costs, total_profit, average_vehicle_mileage    # Return calculated values

    def query_update_availability(self, vehicle_id, available: bool):
        """Updates the availability status of a vehicle.
        
        Args:
            vehicle_id (int): ID of the vehicle to update
            available (bool): New availability status (True for available, False for unavailable)
        """
        self.database.execute_query(                        # Executes an update on existing database row
            operation=SQL.OPERATION.UPDATE,                 # Indicates an SQL UPDATE operation
            table=SQL.TABLE.VEHICLES,                       # Target table
            columns=["available"],                          # Column to update
            values=[1 if available else 0],                 # Set availability status
            where=f"id = {vehicle_id}",                     # Matches the vehicle with the same ID
        )
        self.database.commit()                              # This command tells the database to 'write' our new information into the DB

    def query_update_maintenance_mileage(self, vehicle_id):
        """Updates the maintenance mileage for a vehicle.
        
        Args:
            vehicle_id (int): ID of the vehicle to update
        """
        current_mileage = self.database.execute_query(             # Requests database for vehicle data
            operation=SQL.OPERATION.SELECT,                        # Indicates an SQL SELECT operation
            table=SQL.TABLE.VEHICLES,                              # Target table
            columns=["current_mileage"],                           # Specifies variable names whose values are needed
            where=f"id = {vehicle_id}",                            # Matches the vehicle with the same ID
            fetch=SQL.FETCH.ONE,                                   # Fetch a single record
        )[0]                                                       # fetchone() operation returns a tuple, so we obtain the single value in it

        self.database.execute_query(                                # Request specific info from database
            operation=SQL.OPERATION.UPDATE,                         # Indicates an SQL UPDATE operation
            table=SQL.TABLE.VEHICLES,                               # Target table
            columns=["maintenance_mileage"],                        # The column we wish to change
            values=[current_mileage + 10000],                       # New value of the column
            where=f"id = {vehicle_id}",                             # Checks the vehicle IDs match
        )

        self.database.commit()                                      # Update database

    def query_booking(self, vehicle_id, rental_days, estimated_km, customer_name):
        """Books a vehicle, estimates cost, and updates the database.
        
        Args:
            vehicle_id (int): ID of the vehicle to book
            rental_days (int): Number of days for the rental
            estimated_km (int): Estimated kilometers to be driven
            customer_name (str): Name of the customer
            
        Returns:
            float: Total estimated cost for the booking, or None if booking failed
        """
        vehicle = self.database.execute_query(                          # Requests database for vehicle data
            operation=SQL.OPERATION.SELECT,                             # Indicates an SQL SELECT operation
            table=SQL.TABLE.VEHICLES,                                   # Target table
            columns=["daily_price", "maintenance_cost", "available"],   # Specifies variable names whose values are needed
            where=f"id = {vehicle_id}",                                 # Matches the vehicle with the same ID
            fetch=SQL.FETCH.ONE,                                        # Fetch a single record
        )

        if not vehicle and not vehicle[2]:                              # Checks vehicle's existance in database and its 3rd value ('available')
            return None                                                 # Returns falsy value

        daily_price, maintenance_cost, _ = vehicle                      # Unpacks needed values from vehicle

        mileage_cost = maintenance_cost * estimated_km                  # Calculates price to be paid for every driven km
        duration_cost = daily_price * rental_days                       # Calculates price to be paid for every rented day
        total_estimated_cost = duration_cost + mileage_cost             # Adds both costs

        self.database.execute_query(                                                                    # Insert booking record in database
            operation=SQL.OPERATION.INSERT,                                                             # Indicates an SQL INSERT operation
            table=SQL.TABLE.BOOKINGS,                                                                   # Target table
            columns=["vehicle_id", "rental_days", "estimated_km", "estimated_cost", "customer_name"],   # Variable names we look for
            values=[vehicle_id, rental_days, estimated_km, total_estimated_cost, customer_name],        # Values to be put into columns
        )

        self.database.execute_query(                                                                                        # Insert log record in database
            operation=SQL.OPERATION.INSERT,                                                                                 # Indicates an SQL INSERT operation
            table=SQL.TABLE.LOGS,                                                                                           # Target table
            columns=["vehicle_id", "rental_duration", "revenue", "additional_costs", "customer_name", "transaction_type"],  # Variable names we look for
            values=[vehicle_id, rental_days, total_estimated_cost, 0, customer_name, "booking"],                            # Values to be put into columns
        )

        self.database.execute_query(                    # Mark vehicle as unavailable in database
            operation=SQL.OPERATION.UPDATE,             # Indicates an SQL UPDATE operation
            table=SQL.TABLE.VEHICLES,                   # Target table
            columns=["available"],                      # The column we wish to change
            values=[0],                                 # New value of the column
            where=f"id = {vehicle_id}",                 # Matches the vehicle with the same ID
        )

        self.database.commit()                          # This command tells the database to 'write' our new information into the DB
        return total_estimated_cost                     # Returns total value to be paid by the customer when returning the vehicle

    def query_return(self, vehicle_id, actual_km, late_days, customer_name):
        """Updates a vehicles availability and calculates the rental costs.
        
        Args:
            vehicle_id (int): ID of the vehicle being returned
            actual_km (int): Actual kilometers driven during rental
            late_days (int): Number of days the return was late
            customer_name (str): Name of the customer returning the vehicle
            
        Returns:
            float: Total revenue from the rental, or None if return failed
        """
        vehicle = self.database.execute_query(      # Requests database for a vehicle data
            operation=SQL.OPERATION.SELECT,         # Indicates an SQL SELECT operation
            table=SQL.TABLE.VEHICLES,               # Target table
            where=f"id = {vehicle_id}",             # Matches the vehicle with the same ID
            fetch=SQL.FETCH.ONE,                    # Fetch a single record
        )

        if not vehicle:                             # Checks if vehicle exists
            return None                             # Returns a falsy value if so

        booking = self.database.execute_query(      # Checks database for booked vehicle
            operation=SQL.OPERATION.SELECT,         # Indicates an SQL SELECT operation
            table=SQL.TABLE.BOOKINGS,               # Target table
            where=f"vehicle_id = {vehicle_id}",     # Matches the vehicle with the same ID
            fetch=SQL.FETCH.ONE,                    # Fetch a single record
        )

        if not booking:                             # Checks if the booking exists
            return None                             # Vehicle is not currently booked, returns falsy value

        current_mileage = vehicle[3]                # Assuming column 3 is 'current_mileage', retrieves said value
        rental_days = booking[2]                    # Assuming column 2 is 'rental_days', retrieves said value
        estimated_km = booking[3]                   # Assuming column 3 is 'estimated_km', retrieves said value
        estimated_cost = booking[4]                 # Assuming column 4 is 'estimated_cost', retrieves said value

        cleaning_fees = 20                                                      # Static value, used for every vehicle
        lateness_fee = late_days * 10                                           # Charge 10€ per late day
        exceeded_kms = max(0, actual_km - estimated_km)                         # Checks if driven kms exceed expected kms, otherwise, returns 0
        exceeded_mileage_fee = exceeded_kms * 0.5                               # Adds 0.5€ per extra km
        additional_costs = exceeded_mileage_fee + lateness_fee + cleaning_fees  # Sums all extra costs
        total_revenue = estimated_cost + additional_costs                       # All the costs are put together (revenue for the company)

        new_mileage = current_mileage + actual_km                               # Adds driven mileage to the current_mileage

        self.database.execute_query(                                            # Deletes this booking from the table
            operation=SQL.OPERATION.DELETE,                                     # Indicates an SQL DELETE operation
            table=SQL.TABLE.BOOKINGS,                                           # Target table
            where=f"vehicle_id = {vehicle_id}",                                 # Looks for matching ID
        )

        self.database.execute_query(                            # Updates the 'vehicles' table to change the driven mileage and availability of a vehicle
            operation=SQL.OPERATION.UPDATE,                     # Indicates an SQL UPDATE operation
            table=SQL.TABLE.VEHICLES,                           # Target table
            columns=["current_mileage", "available"],           # Variables which will receive the update
            values=[new_mileage, 1],                            # New values for specified 'columns'
            where=f"id = {vehicle_id}",                         # Looks for matching ID
        )

        self.database.execute_query(                                                                                        # Creates a new log in the DB with 'return' type
            operation=SQL.OPERATION.INSERT,                                                                                 # Indicates an SQL INSERT operation
            table=SQL.TABLE.LOGS,                                                                                           # Target table
            columns=["vehicle_id", "rental_duration", "revenue", "additional_costs", "customer_name", "transaction_type"],  # Initializes variables in the new row
            values=[vehicle_id, rental_days, total_revenue, additional_costs, customer_name, "return"],                     # Introduces values for the new row
        )

        self.database.commit()                                          # This command tells the database to 'write' our new information into the DB
        return total_revenue                                            # Returns the total earnings made on this vehicle's booking to be later displayed

    def close(self):
        """Sends a 'close' signal to the database object."""
        self.database.close()