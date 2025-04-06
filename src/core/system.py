from src.misc.utilities import load_data, save_data
from src.misc.constants import TABLES, ATTRIBUTES

VEHICLES, BOOKINGS, LOGS = (
    TABLES.VEHICLES,
    TABLES.BOOKINGS,
    TABLES.LOGS,
)

ID, BRAND, MODEL, CURRENT_MILEAGE, DAILY_PRICE, MAINTENANCE_COST, MAINTENANCE_MILEAGE, AVAILABLE, VEHICLE_ID, CUSTOMER_NAME, RENTAL_DURATION, ESTIMATED_KM, ESTIMATED_COST, REVENUE, ADDITIONAL_COSTS, TRANSACTION_TYPE = (
    ATTRIBUTES.ID, ATTRIBUTES.BRAND, ATTRIBUTES.MODEL, ATTRIBUTES.CURRENT_MILEAGE, ATTRIBUTES.DAILY_PRICE,
    ATTRIBUTES.MAINTENANCE_COST, ATTRIBUTES.MAINTENANCE_MILEAGE, ATTRIBUTES.AVAILABLE, ATTRIBUTES.VEHICLE_ID,
    ATTRIBUTES.CUSTOMER_NAME, ATTRIBUTES.RENTAL_DURATION, ATTRIBUTES.ESTIMATED_KM, ATTRIBUTES.ESTIMATED_COST,
    ATTRIBUTES.REVENUE, ATTRIBUTES.ADDITIONAL_COSTS, ATTRIBUTES.TRANSACTION_TYPE
)

class System:
    def __init__(self):
        self.data = load_data()
        tables, counters = self.data["tables"], self.data["counters"]
        
        self.vehicles_count = counters[VEHICLES]
        self.bookings_count = counters[BOOKINGS]
        self.logs_count = counters[LOGS]

        self.vehicles = tables[VEHICLES]
        self.bookings = tables[BOOKINGS]
        self.logs = tables[LOGS]
    
    def add_vehicle(self, brand, model, mileage, daily_price, maintenance_cost):
        self.vehicles_count += 1
        self.vehicles.append({
            ID: self.vehicles_count,
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
        self.bookings_count += 1
        self.bookings.append({
            ID: self.bookings_count,
            VEHICLE_ID: vehicle_id,
            CUSTOMER_NAME: customer_name,
            RENTAL_DURATION: rental_duration,
            ESTIMATED_KM: estimated_km,
            ESTIMATED_COST: estimated_cost,
        })
        save_data(self.data)

    def add_log(self, vehicle_id, customer_name, rental_duration, revenue, additional_costs, transaction_type):
        self.logs_count += 1
        self.logs.append({
            ID: self.logs_count,
            VEHICLE_ID: vehicle_id,
            CUSTOMER_NAME: customer_name,
            RENTAL_DURATION: rental_duration,
            REVENUE: revenue,
            ADDITIONAL_COSTS: additional_costs,
            TRANSACTION_TYPE: transaction_type
        })
        save_data(self.data)
    
    def get_vehicles_requiring_maintenance(self):
        return [v for v in self.vehicles if v[CURRENT_MILEAGE] >= v[MAINTENANCE_MILEAGE]]
    
    def get_unavailable_vehicles(self):
        return [v for v in self.vehicles if not v[AVAILABLE]]
    
    def get_table_row(self, table_name, column_name, column_value):
        return [record for record in self.data.get(table_name, []) if column_name in record and str(record[column_name]) == str(column_value)]
    
    def get_customer_name(self, vehicle_id):
        return next((b[CUSTOMER_NAME] for b in self.bookings if b[VEHICLE_ID] == vehicle_id), None)
    
    def get_financial_metrics(self):
        return_logs = (log for log in self.logs if log[TRANSACTION_TYPE] == "return")
        if not return_logs:
            return ()
        
        total_revenue = sum(log[REVENUE] for log in return_logs)
        total_additional_costs = sum(log[ADDITIONAL_COSTS] for log in return_logs)
        total_maintenance_cost = sum(v[MAINTENANCE_COST] for v in self.vehicles)
        avg_mileage = sum(v[CURRENT_MILEAGE] for v in self.vehicles) / len(self.vehicles) if self.vehicles else 0

        total_operational_costs = total_maintenance_cost + total_additional_costs
        total_profit = total_revenue - total_operational_costs
        
        return total_revenue, total_operational_costs, total_profit, avg_mileage
    
    def query_update_availability(self, vehicle_id, available):
        for v in self.vehicles:
            if v[ID] == vehicle_id:
                v[AVAILABLE] = available
                save_data(self.data)
                return True
        return False
    
    def query_update_current_mileage(self, vehicle_id, new_mileage):
        for v in self.vehicles:
            if v[ID] == vehicle_id:
                v[CURRENT_MILEAGE] = new_mileage
                save_data(self.data)
                return True
        return False
    
    def query_update_maintenance_mileage(self, vehicle_id):
        for v in self.vehicles:
            if v[ID] == vehicle_id and v[MAINTENANCE_MILEAGE] <= v[CURRENT_MILEAGE]:
                v[MAINTENANCE_MILEAGE] = v[CURRENT_MILEAGE] + 10000
                save_data(self.data)
                return True
        return False
    
    def query_booking(self, vehicle_id, rental_duration, estimated_km, customer_name):
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
        vehicle = next((v for v in self.vehicles if v[ID] == vehicle_id), None)
        if not vehicle:
            return None
        
        original_booking = next((b for b in self.bookings if b[VEHICLE_ID] == vehicle_id), None)
        if not original_booking:
            return None

        self.bookings = [b for b in self.bookings if b[VEHICLE_ID] != vehicle_id] # We create a new 'bookings' table without this one
        cleaning_fees = 20.0                                                      # Static value, used for every vehicle
        lateness_fee = late_days * 10.0                                           # Charge 10€ per late day
        driven_kms = max(0, actual_km - original_booking[ESTIMATED_KM])                         # Checks if driven kms exceed expected kms, otherwise, returns 0
        driven_kms_fee = driven_kms * 1.0                                           # Adds 1€ per kilometer
        additional_costs = driven_kms_fee + lateness_fee + cleaning_fees  # Sums all extra costs
        total_revenue = original_booking[ESTIMATED_COST] + additional_costs                       # All the costs are put together (revenue for the company)
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
