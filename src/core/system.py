from src.misc.utilities import load_data, save_data
from src.misc.constants import ATTRIBUTES

class System:
    def __init__(self):
        self.data = load_data()
        self.vehicles = self.data["vehicles"]
        self.bookings = self.data["bookings"]
        self.logs = self.data["logs"]
    
    def add_vehicle(self, brand, model, mileage, daily_price, maintenance_cost):
        vehicle = {
            ATTRIBUTES.ID: len(self.vehicles) + 1,
            ATTRIBUTES.BRAND: brand,
            ATTRIBUTES.MODEL: model,
            ATTRIBUTES.DAILY_PRICE: daily_price,
            ATTRIBUTES.MAINTENANCE_COST: maintenance_cost,
            ATTRIBUTES.CURRENT_MILEAGE: mileage,
            ATTRIBUTES.MAINTENANCE_MILEAGE: mileage + 10000,
            ATTRIBUTES.AVAILABLE: True
        }
        self.vehicles.append(vehicle)
        save_data(self.data)
    
    def get_vehicles_requiring_maintenance(self):
        return [v for v in self.vehicles if v[ATTRIBUTES.CURRENT_MILEAGE] >= v[ATTRIBUTES.MAINTENANCE_MILEAGE]]
    
    def get_unavailable_vehicles(self):
        return [v for v in self.vehicles if not v[ATTRIBUTES.AVAILABLE]]
    
    def get_table_row(self, table_name, column_name, column_value):
        return [record for record in self.data.get(table_name, []) if column_name in record and str(record[column_name]) == str(column_value)]
    
    def get_customer_name(self, vehicle_id):
        return next((b[ATTRIBUTES.CUSTOMER_NAME] for b in self.bookings if b[ATTRIBUTES.VEHICLE_ID] == vehicle_id), None)
    
    def get_financial_metrics(self):
        return_logs = (log for log in self.logs if log[ATTRIBUTES.TRANSACTION_TYPE] == "return")
        if not return_logs:
            return ()
        
        total_revenue = sum(log[ATTRIBUTES.REVENUE] for log in return_logs)
        total_additional_costs = sum(log[ATTRIBUTES.ADDITIONAL_COSTS] for log in return_logs)
        total_maintenance_cost = sum(v[ATTRIBUTES.MAINTENANCE_COST] for v in self.vehicles)
        avg_mileage = sum(v[ATTRIBUTES.CURRENT_MILEAGE] for v in self.vehicles) / len(self.vehicles) if self.vehicles else 0

        total_operational_costs = total_maintenance_cost + total_additional_costs
        total_profit = total_revenue - total_operational_costs
        
        return total_revenue, total_operational_costs, total_profit, avg_mileage
    
    def query_update_availability(self, vehicle_id, available):
        for v in self.vehicles:
            if v[ATTRIBUTES.ID] == vehicle_id:
                v[ATTRIBUTES.AVAILABLE] = available
                save_data(self.data)
                return True
        return False
    
    def query_update_current_mileage(self, vehicle_id, new_mileage):
        for v in self.vehicles:
            if v[ATTRIBUTES.ID] == vehicle_id:
                v[ATTRIBUTES.CURRENT_MILEAGE] = new_mileage
                save_data(self.data)
                return True
        return False
    
    def query_update_maintenance_mileage(self, vehicle_id):
        for v in self.vehicles:
            if v[ATTRIBUTES.ID] == vehicle_id:
                v[ATTRIBUTES.MAINTENANCE.MILEAGE] = v[ATTRIBUTES.CURRENT_MILEAGE] + 10000
                save_data(self.data)
                return True
        return False
    
    def query_booking(self, vehicle_id, rental_duration, estimated_km, customer_name):
        vehicle = next((v for v in self.vehicles if v[ATTRIBUTES.ID] == vehicle_id and v[ATTRIBUTES.AVAILABLE]), None)
        if not vehicle:
            return None
        
        mileage_cost = vehicle[ATTRIBUTES.MAINTENANCE_COST] * estimated_km
        duration_cost = vehicle[ATTRIBUTES.DAILY_PRICE] * rental_duration
        total_estimated_cost = float(duration_cost + mileage_cost)
        
        self.bookings.append({
            ATTRIBUTES.ID: len(self.bookings) + 1,
            ATTRIBUTES.VEHICLE_ID: vehicle_id,
            ATTRIBUTES.RENTAL_DURATION: rental_duration,
            ATTRIBUTES.ESTIMATED_KM: estimated_km,
            ATTRIBUTES.ESTIMATED_COST: total_estimated_cost,
            ATTRIBUTES.CUSTOMER_NAME: customer_name
        })
        
        self.logs.append({
            ATTRIBUTES.ID: len(self.logs) + 1,
            ATTRIBUTES.VEHICLE_ID: vehicle_id,
            ATTRIBUTES.RENTAL_DURATION: rental_duration,
            ATTRIBUTES.REVENUE: total_estimated_cost,
            ATTRIBUTES.ADDITIONAL_COSTS: 0.0,
            ATTRIBUTES.CUSTOMER_NAME: customer_name,
            ATTRIBUTES.TRANSACTION_TYPE: "booking"
        })
        
        self.query_update_availability(vehicle_id, False)
        return total_estimated_cost
    
    def query_return(self, vehicle_id, customer_name, actual_km, late_days):
        vehicle = next((v for v in self.vehicles if v[ATTRIBUTES.ID] == vehicle_id), None)
        if not vehicle:
            return None
        
        original_booking = next((b for b in self.bookings if b[ATTRIBUTES.VEHICLE_ID] == vehicle_id), None)
        if not original_booking:
            return None

        cleaning_fees = 20.0                                                      # Static value, used for every vehicle
        lateness_fee = late_days * 10.0                                           # Charge 10€ per late day
        driven_kms = max(0, actual_km - original_booking[ATTRIBUTES.ESTIMATED_KM])                         # Checks if driven kms exceed expected kms, otherwise, returns 0
        driven_kms_fee = driven_kms * 1.0                               # Adds 1€ per 
        additional_costs = driven_kms_fee + lateness_fee + cleaning_fees  # Sums all extra costs
        total_revenue = original_booking[ATTRIBUTES.ESTIMATED_COST] + additional_costs                       # All the costs are put together (revenue for the company)
        current_mileage = next((v[ATTRIBUTES.CURRENT_MILEAGE] for v in self.vehicles if v[ATTRIBUTES.ID] == original_booking[ATTRIBUTES.VEHICLE_ID]), 0)
        new_mileage = current_mileage + actual_km
        final_rental_duration = original_booking[ATTRIBUTES.RENTAL_DURATION] + late_days

        self.logs.append({
            ATTRIBUTES.ID: len(self.logs) + 1,
            ATTRIBUTES.VEHICLE_ID: vehicle_id,
            ATTRIBUTES.RENTAL_DURATION: final_rental_duration,
            ATTRIBUTES.REVENUE: total_revenue,
            ATTRIBUTES.ADDITIONAL_COSTS: lateness_fee,
            ATTRIBUTES.CUSTOMER_NAME: customer_name,
            ATTRIBUTES.TRANSACTION_TYPE: "return"
        })
        
        self.query_update_current_mileage(vehicle_id, new_mileage)
        self.query_update_availability(vehicle_id, True)
        return total_revenue
