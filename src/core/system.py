from src.core.database import load_data, save_data      # Importing database functionality
from src.misc.constants import TABLES, ATTRIBUTES       # Importing namespaces with common string variables
from copy import deepcopy                               # Import a module to create a copy of objects like dictionaries to the root

ID, BRAND, MODEL, CURRENT_MILEAGE, DAILY_PRICE, MAINTENANCE_COST, MAINTENANCE_MILEAGE, AVAILABLE, VEHICLE_ID, CUSTOMER_NAME, RENTAL_DURATION, ESTIMATED_KM, ESTIMATED_COST, REVENUE, ADDITIONAL_COSTS, TRANSACTION_TYPE = (
    ATTRIBUTES.ID, ATTRIBUTES.BRAND, ATTRIBUTES.MODEL, ATTRIBUTES.CURRENT_MILEAGE, ATTRIBUTES.DAILY_PRICE,
    ATTRIBUTES.MAINTENANCE_COST, ATTRIBUTES.MAINTENANCE_MILEAGE, ATTRIBUTES.AVAILABLE, ATTRIBUTES.VEHICLE_ID,
    ATTRIBUTES.CUSTOMER_NAME, ATTRIBUTES.RENTAL_DURATION, ATTRIBUTES.ESTIMATED_KM, ATTRIBUTES.ESTIMATED_COST,
    ATTRIBUTES.REVENUE, ATTRIBUTES.ADDITIONAL_COSTS, ATTRIBUTES.TRANSACTION_TYPE     # De-structures the ATTRIBUTES namespace to avoid redundancy on other parts of the code
)

class System:
    """A class representing the vehicle rental system that manages vehicles, bookings, and financial logs."""
    
    def __init__(self):
        """Initialize the System by loading data from the database and setting up tables and counters."""
        self.data = load_data()                                                                 # Obtain the database content (a dictionary with dictionaries)
        self.tables, self.counters = self.data["tables"], self.data["counters"]                 # Separate the two main dictionaries: the counters and the tables
        self.vehicles = self.tables[TABLES.VEHICLES]                                            # We get the reference to the 'vehicles' table
        self.bookings = self.tables[TABLES.BOOKINGS]                                            # We get the reference to the 'bookings' table
        self.logs = self.tables[TABLES.LOGS]                                                    # We get the reference to the 'logs' table

    def __del__(self):
        """Whenever a System instance gets deleted, it will save all the database values as they are."""
        self.save_all()

    def save_all(self):
        save_data(self.data)
    
    def add_vehicle(self, brand, model, mileage, daily_price, maintenance_cost):
        """
        Add a new vehicle to the system.
        
        Args:
            brand (str): The brand of the vehicle
            model (str): The model of the vehicle
            mileage (float): Current mileage of the vehicle
            daily_price (float): Daily rental price of the vehicle
            maintenance_cost (float): Cost per km for maintenance
        """
        self.counters[TABLES.VEHICLES] += 1             # Increase the vehicles' counter (by reference)
        self.vehicles.append({                          # Add a dictionary (object) with the values to be stored
            ID: self.counters[TABLES.VEHICLES],         # The 'id' attribute
            BRAND: brand,                               # The 'brand' attribute
            MODEL: model,                               # The 'model' attribute
            DAILY_PRICE: daily_price,                   # The 'daily_price' attribute
            MAINTENANCE_COST: maintenance_cost,         # The 'maintenance_cost' attribute
            CURRENT_MILEAGE: mileage,                   # The 'current_mileage' attribute
            MAINTENANCE_MILEAGE: mileage + 10000,       # The 'maintenance_mileage' attribute
            AVAILABLE: True                             # The 'available' attribute
        })
        self.save_all()                                 # Stores data into the .pkl file

    def add_booking(self, vehicle_id, customer_name, rental_duration, estimated_km, estimated_cost):
        """
        Add a new booking to the system.
        
        Args:
            vehicle_id (int): ID of the vehicle being booked
            customer_name (str): Name of the customer making the booking
            rental_duration (int): Duration of the rental in days
            estimated_km (float): Estimated kilometers for the rental
            estimated_cost (float): Estimated total cost of the rental
        """
        self.counters[TABLES.BOOKINGS] += 1             # Increase the bookings' counter (by reference)
        self.bookings.append({                          # Add a dictionary (object) with the values to be stored
            ID: self.counters[TABLES.BOOKINGS],         # The 'id' attribute
            VEHICLE_ID: vehicle_id,                     # The 'vehicle_id' attribute
            CUSTOMER_NAME: customer_name,               # The 'customer_name' attribute
            RENTAL_DURATION: rental_duration,           # The 'rental_duration' attribute
            ESTIMATED_KM: estimated_km,                 # The 'estimated_km' attribute
            ESTIMATED_COST: estimated_cost,             # The 'estimated_cost' attribute
        })
        self.save_all()                                 # Stores data into the .pkl file

    def add_log(self, vehicle_id, customer_name, rental_duration, revenue, additional_costs, transaction_type):
        """
        Add a financial log entry to the system.
        
        Args:
            vehicle_id (int): ID of the vehicle involved
            customer_name (str): Name of the customer involved
            rental_duration (int): Duration of the rental in days
            revenue (float): Revenue generated from the transaction
            additional_costs (float): Any additional costs incurred
            transaction_type (str): Type of transaction ('booking' or 'return')
        """
        self.counters[TABLES.LOGS] += 1                     # Increase the logs' counter (by reference)
        self.logs.append({                                  # Add a dictionary (object) with the values to be stored
            ID: self.counters[TABLES.LOGS],                 # The 'id' attribute
            VEHICLE_ID: vehicle_id,                         # The 'vehicle_id' attribute
            CUSTOMER_NAME: customer_name,                   # The 'customer_name' attribute
            RENTAL_DURATION: rental_duration,               # The 'rental_duration' attribute
            REVENUE: revenue,                               # The 'revenue' attribute
            ADDITIONAL_COSTS: additional_costs,             # The 'additional_costs' attribute
            TRANSACTION_TYPE: transaction_type              # The 'transaction_type' attribute
        })
        self.save_all()                                     # Stores data into the .pkl file
    
    def get_vehicles_requiring_maintenance(self):
        """
        Get a list of vehicles that require maintenance (have been used for at least 10,000kms since last maintenance).
        
        Returns:
            list: Vehicles where current mileage exceeds maintenance mileage
        """
        return [v for v in deepcopy(self.vehicles) if v[CURRENT_MILEAGE] >= v[MAINTENANCE_MILEAGE]]
    
    def get_unavailable_vehicles(self):
        """
        Get a list of currently unavailable vehicles.
        
        Returns:
            list: Vehicles marked as unavailable
        """
        return [v for v in deepcopy(self.vehicles) if not v[AVAILABLE]]
    
    def get_table_row(self, table_name, column_name, column_value):
        """
        Search for records in a table where a column contains a specific value.
        
        Args:
            table_name (str): Name of the table to search
            column_name (str): Name of the column to search
            column_value (str): Value to search for in the column
            
        Returns:
            list: Matching records
        """
        return [record for record in deepcopy(self.tables.get(table_name, [])) if str(column_value).lower() in str(record[column_name]).lower()]
    
    def get_customer_name(self, vehicle_id):
        """
        Get the name of the customer who booked a specific vehicle.
        
        Args:
            vehicle_id (int): ID of the vehicle
            
        Returns:
            str: Customer name if found, None otherwise
        """
        return next((b[CUSTOMER_NAME] for b in deepcopy(self.bookings) if b[VEHICLE_ID] == vehicle_id), None)
    
    def get_financial_metrics(self):
        """
        Calculate financial metrics for the rental system.
        
        Returns:
            tuple: Contains (total_revenue, total_operational_costs, total_profit, avg_mileage)
                    or empty tuple if no 'return' logs are found
        """
        return_logs = [log for log in deepcopy(self.logs) if log[TRANSACTION_TYPE] == "return"]           # Return a list with logs whose transaction_type is 'return'
        if not return_logs:                                                                     # Checks if any was found
            return ()                                                                           # Returns empty tuple if none were found
        
        vehicles_copy = deepcopy(self.vehicles)                                                 # Generate a copy of data to avoid data corruption
        total_revenue = sum(log[REVENUE] for log in return_logs)                                # Generates a list of all the return logs' revenues and then adds them up
        total_additional_costs = sum(log[ADDITIONAL_COSTS] for log in return_logs)              # Generates a list of all the return logs' additional_costs and then adds them up
        total_maintenance_cost = sum(v[MAINTENANCE_COST] for v in vehicles_copy)                # Generates a list of all the vehicles' maintenance_cost and then adds them up
        avg_mileage = sum(v[CURRENT_MILEAGE] for v in vehicles_copy) / len(vehicles_copy)       # Generates a list of all the vehicles' current_mileage, adds them up and then divides them by the amount of vehicles
        total_operational_costs = total_maintenance_cost + total_additional_costs               # Adds two different types of costs
        total_profit = total_revenue - total_operational_costs                                  # Takes the total of payments and substracts the costs of operations
        
        return total_revenue, total_operational_costs, total_profit, avg_mileage                # Returns a tuple with the results
    
    def query_update_availability(self, vehicle_id, available):
        """
        Update the availability status of a vehicle.
        
        Args:
            vehicle_id (int): ID of the vehicle to update
            available (bool): New availability status
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        for v in self.vehicles:                     # Iterates over the vehicles' table
            if v[ID] == vehicle_id:                 # Checks if any of them match the given id
                v[AVAILABLE] = available            # Changes the 'available' attribute to the given value
                self.save_all()                # Stores the new info in the .pkl database
                return True                         # Returns True as a sign of success
        return False                                # Returns False as a sign of failure, in case no vehicle was found
    
    def query_update_current_mileage(self, vehicle_id, new_mileage):
        """
        Update the current mileage of a vehicle.
        
        Args:
            vehicle_id (int): ID of the vehicle to update
            new_mileage (float): New mileage value
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        for v in self.vehicles:                         # Iterates over the vehicles' table
            if v[ID] == vehicle_id:                     # Checks if any of them match the given id
                v[CURRENT_MILEAGE] = new_mileage        # Changes current_mileage to the given value
                self.save_all()                    # Stores info in .pkl database
                return True                             # Returns True as a sign of success
        return False                                    # Returns False if no vehicle was found
    
    def query_update_maintenance_mileage(self, vehicle_id):
        """
        Update the maintenance mileage threshold for a vehicle if current mileage exceeds it.
        
        Args:
            vehicle_id (int): ID of the vehicle to update
            
        Returns:
            bool: True if update was performed, False otherwise
        """
        for v in self.vehicles:                                                         # Iterates over the vehicles' table
            if v[ID] == vehicle_id and v[MAINTENANCE_MILEAGE] <= v[CURRENT_MILEAGE]:    # Checks if any of them match the given id and the vehicle actually needs maintenance
                v[MAINTENANCE_MILEAGE] = v[CURRENT_MILEAGE] + 10000                     # Changes maintenance_mileage to the new value
                self.save_all()                                                    # Stores info in .pkl database
                return True                                                             # Returns True as a sign of success
        return False                                                                    # Returns False if no vehicle was found
    
    def query_booking(self, vehicle_id, customer_name, rental_duration, estimated_km):
        """
        Process a vehicle booking request.
        
        Args:
            vehicle_id (int): ID of the vehicle to book
            rental_duration (int): Duration of the rental in days
            estimated_km (float): Estimated kilometers for the rental
            customer_name (str): Name of the customer making the booking
            
        Returns:
            float: Total estimated cost if booking was successful, None otherwise
        """
        vehicle = next((v for v in deepcopy(self.vehicles) if v[ID] == vehicle_id and v[AVAILABLE]), None)    # Iterates over vehicles' table until finding match, otherwise, return None
        if not vehicle:                                                                                       # Checks if vehicle was found
            return None                                                                                       # Returns 'None' otherwise
        
        mileage_cost = vehicle[MAINTENANCE_COST] * estimated_km         # Multiplies vehicle's maintenance_cost times kms to be driven
        duration_cost = vehicle[DAILY_PRICE] * rental_duration          # Multiplies vehicle's daily_price times the days to be rented
        total_estimated_cost = float(duration_cost + mileage_cost)      # Adds the two previous values and turns them to floating value
        
        self.add_booking(                           # Adds new booking instance to DB
            vehicle_id=vehicle_id,                  # Sets param to be stored
            customer_name=customer_name,            # Sets param to be stored
            rental_duration=rental_duration,        # Sets param to be stored
            estimated_km=estimated_km,              # Sets param to be stored
            estimated_cost=total_estimated_cost     # Sets param to be stored
        )
        
        self.add_log(                               # Adds new log instance to DB
            vehicle_id=vehicle_id,                  # Sets param to be stored
            customer_name=customer_name,            # Sets param to be stored
            rental_duration=rental_duration,        # Sets param to be stored
            revenue=total_estimated_cost,           # Sets param to be stored
            additional_costs=0.0,                   # Sets param to be stored
            transaction_type="booking",             # Sets param to be stored
        )
        
        self.query_update_availability(vehicle_id, False)   # Updates a vehicle's availability to False (unavailable)
        self.save_all()                                # Stores new info into .pkl database
        return total_estimated_cost                         # Returns the probable cost (for the client) that will be paid in the future
    
    def query_return(self, vehicle_id, customer_name, actual_km, late_days):
        """
        Process a vehicle return.
        
        Args:
            vehicle_id (int): ID of the vehicle being returned
            customer_name (str): Name of the customer returning the vehicle
            actual_km (float): Actual kilometers driven during rental
            late_days (int): Number of days the return is late
            
        Returns:
            float: Total revenue generated from the rental including any fees, None if vehicle not found
        """
        vehicles_copy = deepcopy(self.vehicles)                                                 # Creates a copy of the table to avoid accidental changes
        vehicle = next((v for v in vehicles_copy if v[ID] == vehicle_id), None)                 # Search for a vehicle matching the id, or return None
        if not vehicle:                                                                         # Check if vehicle was found
            return None                                                                         # Return None if not found
        
        bookings_copy = deepcopy(self.bookings)                                                     # Creates a copy of the table to avoid accidental changes
        original_booking = next((b for b in bookings_copy if b[VEHICLE_ID] == vehicle_id), None)    # Search for a booked vehicle if id matches, or return None
        if not original_booking:                                                                    # Check if booking was found
            return None                                                                             # Return None if not found

        self.bookings = [b for b in bookings_copy if b[VEHICLE_ID] != vehicle_id]                                 # Create a new list of bookings without the other one (deleting it)
        cleaning_fee = 20.0                                                                                                 # Predefined value of cleaning fee to avoid discrepancies
        lateness_fee = late_days * 10.0                                                                                     # For every late day, 10 euros are charged
        driven_kms_fee = actual_km * 1.0                                                                                    # Take all the driven kms and charge 1 euro for them
        additional_costs = driven_kms_fee + lateness_fee + cleaning_fee                                                     # Add up all the extra charges made
        total_revenue = original_booking[ESTIMATED_COST] + additional_costs                                                 # Obtain the total of earnings from the booking's payment plus any other fee
        current_mileage = next((v[CURRENT_MILEAGE] for v in vehicles_copy if v[ID] == original_booking[VEHICLE_ID]), 0)     # Iterate over the vehicles' table to find its current_mileage value
        new_mileage = current_mileage + actual_km                                                                           # Add the current_mileage with the driven kms
        final_rental_duration = original_booking[RENTAL_DURATION] + late_days                                               # Add the estimated rental time plus any late days

        self.add_log(                                                 # Adds new log instance to DB
            vehicle_id=vehicle_id,                                    # Sets param to be stored
            customer_name=customer_name,                              # Sets param to be stored
            rental_duration=final_rental_duration,                    # Sets param to be stored
            revenue=total_revenue,                                    # Sets param to be stored
            additional_costs=additional_costs,                        # Sets param to be stored
            transaction_type="return",                                # Sets param to be stored
        )
        
        self.query_update_current_mileage(vehicle_id, new_mileage)      # Update returned vehicle's total mileage
        self.query_update_availability(vehicle_id, True)                # Update returned vehicle's availability (is now available)
        self.save_all()                                            # Store new info into .pkl database
        return total_revenue                                            # Return final revenue (for business) to be displayed