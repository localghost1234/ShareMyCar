from src.core.database import load_data, save_data  # Importing database functionality
from src.misc.constants import TABLES, ATTRIBUTES   # Importing namespaces with common string variables

ID, BRAND, MODEL, CURRENT_MILEAGE, DAILY_PRICE, MAINTENANCE_COST, MAINTENANCE_MILEAGE, AVAILABLE, VEHICLE_ID, CUSTOMER_NAME, RENTAL_DURATION, ESTIMATED_KM, ESTIMATED_COST, REVENUE, ADDITIONAL_COSTS, TRANSACTION_TYPE = (
    ATTRIBUTES.ID, ATTRIBUTES.BRAND, ATTRIBUTES.MODEL, ATTRIBUTES.CURRENT_MILEAGE, ATTRIBUTES.DAILY_PRICE,
    ATTRIBUTES.MAINTENANCE_COST, ATTRIBUTES.MAINTENANCE_MILEAGE, ATTRIBUTES.AVAILABLE, ATTRIBUTES.VEHICLE_ID,
    ATTRIBUTES.CUSTOMER_NAME, ATTRIBUTES.RENTAL_DURATION, ATTRIBUTES.ESTIMATED_KM, ATTRIBUTES.ESTIMATED_COST,
    ATTRIBUTES.REVENUE, ATTRIBUTES.ADDITIONAL_COSTS, ATTRIBUTES.TRANSACTION_TYPE                # We de-structure the ATTRIBUTES namespace to avoid redundancy on other parts
)

class System:
    """A class representing the vehicle rental system that manages vehicles, bookings, and financial logs."""
    
    def __init__(self):
        """Initialize the System by loading data from the database and setting up tables and counters."""
        self.data = load_data()
        self.tables, self.counters = self.data["tables"], self.data["counters"]
        self.vehicles = self.tables[TABLES.VEHICLES]
        self.bookings = self.tables[TABLES.BOOKINGS]
        self.logs = self.tables[TABLES.LOGS]

    def __del__(self):
        """Whenever a System instance gets deleted, it will save all the database values as they are."""
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
        self.counters[TABLES.VEHICLES] += 1
        self.vehicles.append({
            ID: self.counters[TABLES.VEHICLES],
            BRAND: brand,
            MODEL: model,
            DAILY_PRICE: daily_price,
            MAINTENANCE_COST: maintenance_cost,
            CURRENT_MILEAGE: mileage,
            MAINTENANCE_MILEAGE: mileage + 10000,
            AVAILABLE: True
        })
        save_data(self.data)

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
        self.counters[TABLES.BOOKINGS] += 1
        self.bookings.append({
            ID: self.counters[TABLES.BOOKINGS],
            VEHICLE_ID: vehicle_id,
            CUSTOMER_NAME: customer_name,
            RENTAL_DURATION: rental_duration,
            ESTIMATED_KM: estimated_km,
            ESTIMATED_COST: estimated_cost,
        })
        save_data(self.data)

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
        self.counters[TABLES.LOGS] += 1
        self.logs.append({
            ID: self.counters[TABLES.LOGS],
            VEHICLE_ID: vehicle_id,
            CUSTOMER_NAME: customer_name,
            RENTAL_DURATION: rental_duration,
            REVENUE: revenue,
            ADDITIONAL_COSTS: additional_costs,
            TRANSACTION_TYPE: transaction_type
        })
        save_data(self.data)
    
    def get_vehicles_requiring_maintenance(self):
        """
        Get a list of vehicles that require maintenance.
        
        Returns:
            list: Vehicles where current mileage exceeds maintenance mileage
        """
        return [v for v in self.vehicles if v[CURRENT_MILEAGE] >= v[MAINTENANCE_MILEAGE]]
    
    def get_unavailable_vehicles(self):
        """
        Get a list of currently unavailable vehicles.
        
        Returns:
            list: Vehicles marked as unavailable
        """
        return [v for v in self.vehicles if not v[AVAILABLE]]
    
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
        return [record for record in self.tables.get(table_name, []) if str(column_value).lower() in str(record[column_name]).lower()]
    
    def get_customer_name(self, vehicle_id):
        """
        Get the name of the customer who booked a specific vehicle.
        
        Args:
            vehicle_id (int): ID of the vehicle
            
        Returns:
            str: Customer name if found, None otherwise
        """
        return next((b[CUSTOMER_NAME] for b in self.bookings if b[VEHICLE_ID] == vehicle_id), None)
    
    def get_financial_metrics(self):
        """
        Calculate financial metrics for the rental system.
        
        Returns:
            tuple: Contains (total_revenue, total_operational_costs, total_profit, avg_mileage)
                   Returns empty tuple if no return logs exist
        """
        returns_logs = [log for log in self.logs if log[TRANSACTION_TYPE] == "return"]
        if not returns_logs:
            return ()
        
        total_revenue = sum(log[REVENUE] for log in returns_logs)
        total_additional_costs = sum(log[ADDITIONAL_COSTS] for log in returns_logs)
        total_maintenance_cost = sum(v[MAINTENANCE_COST] for v in self.vehicles)
        avg_mileage = sum(v[CURRENT_MILEAGE] for v in self.vehicles) / len(self.vehicles)
        total_operational_costs = total_maintenance_cost + total_additional_costs
        total_profit = total_revenue - total_operational_costs
        
        return total_revenue, total_operational_costs, total_profit, avg_mileage
    
    def query_update_availability(self, vehicle_id, available):
        """
        Update the availability status of a vehicle.
        
        Args:
            vehicle_id (int): ID of the vehicle to update
            available (bool): New availability status
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        for v in self.vehicles:
            if v[ID] == vehicle_id:
                v[AVAILABLE] = available
                save_data(self.data)
                return True
        return False
    
    def query_update_current_mileage(self, vehicle_id, new_mileage):
        """
        Update the current mileage of a vehicle.
        
        Args:
            vehicle_id (int): ID of the vehicle to update
            new_mileage (float): New mileage value
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        for v in self.vehicles:
            if v[ID] == vehicle_id:
                v[CURRENT_MILEAGE] = new_mileage
                save_data(self.data)
                return True
        return False
    
    def query_update_maintenance_mileage(self, vehicle_id):
        """
        Update the maintenance mileage threshold for a vehicle if current mileage exceeds it.
        
        Args:
            vehicle_id (int): ID of the vehicle to update
            
        Returns:
            bool: True if update was performed, False otherwise
        """
        for v in self.vehicles:
            if v[ID] == vehicle_id and v[MAINTENANCE_MILEAGE] <= v[CURRENT_MILEAGE]:
                v[MAINTENANCE_MILEAGE] = v[CURRENT_MILEAGE] + 10000
                save_data(self.data)
                return True
        return False
    
    def query_booking(self, vehicle_id, rental_duration, estimated_km, customer_name):
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
        vehicle = next((v for v in self.vehicles if v[ID] == vehicle_id and v[AVAILABLE]), None)
        if not vehicle:
            return None
        
        mileage_cost = vehicle[MAINTENANCE_COST] * estimated_km
        duration_cost = vehicle[DAILY_PRICE] * rental_duration
        total_estimated_cost = float(duration_cost + mileage_cost)
        
        self.add_booking(
            vehicle_id=vehicle_id,
            customer_name=customer_name,
            rental_duration=rental_duration,
            estimated_km=estimated_km,
            estimated_cost=total_estimated_cost
        )
        
        self.add_log(
            vehicle_id=vehicle_id,
            customer_name=customer_name,
            rental_duration=rental_duration,
            revenue=total_estimated_cost,
            additional_costs=0.0,
            transaction_type="booking",
        )
        
        self.query_update_availability(vehicle_id, False)
        save_data(self.data)
        return total_estimated_cost
    
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
        vehicle = next((v for v in self.vehicles if v[ID] == vehicle_id), None)
        if not vehicle:
            return None
        
        original_booking = next((b for b in self.bookings if b[VEHICLE_ID] == vehicle_id), None)
        if not original_booking:
            return None

        self.bookings = [b for b in self.bookings if b[VEHICLE_ID] != vehicle_id]
        cleaning_fees = 20.0
        lateness_fee = late_days * 10.0
        driven_kms = max(0, actual_km - original_booking[ESTIMATED_KM])
        driven_kms_fee = driven_kms * 1.0
        additional_costs = driven_kms_fee + lateness_fee + cleaning_fees
        total_revenue = original_booking[ESTIMATED_COST] + additional_costs
        current_mileage = next((v[CURRENT_MILEAGE] for v in self.vehicles if v[ID] == original_booking[VEHICLE_ID]), 0)
        new_mileage = current_mileage + actual_km
        final_rental_duration = original_booking[RENTAL_DURATION] + late_days

        self.add_log(
            vehicle_id=vehicle_id,
            customer_name=customer_name,
            rental_duration=final_rental_duration,
            revenue=total_revenue,
            additional_costs=additional_costs,
            transaction_type="return",
        )
        
        self.query_update_current_mileage(vehicle_id, new_mileage)
        self.query_update_availability(vehicle_id, True)
        save_data(self.data)
        return total_revenue