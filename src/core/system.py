from tinydb import TinyDB, Query
from src.misc.constants import DB_NAME

class System:
    def __init__(self):
        self.database = TinyDB(DB_NAME)
        self.vehicles = self.database.table('vehicles')
        self.bookings = self.database.table('bookings')
        self.logs = self.database.table('logs')
    
    def add_vehicle(self, brand, model, mileage, daily_price, maintenance_cost):
        self.vehicles.insert({
            "brand": brand,
            "model": model,
            "current_mileage": mileage,
            "daily_price": daily_price,
            "maintenance_cost": maintenance_cost,
            "maintenance_mileage": mileage + 10000,
            "available": True
        })
    
    def get_all_vehicles(self):
        return self.vehicles.all()
    
    def get_all_bookings(self):
        return self.bookings.all()
    
    def get_all_logs(self):
        return self.logs.all()
    
    def get_vehicles_requiring_maintenance(self):
        Vehicle = Query()
        return self.vehicles.search(Vehicle.current_mileage >= Vehicle.maintenance_mileage)
    
    def get_unavailable_vehicles(self):
        Vehicle = Query()
        return self.vehicles.search(Vehicle.available == False)
    
    def get_table_column(self, table_name, column_name):
        table = self.database.table(table_name)
        return [record[column_name] for record in table.all() if column_name in record]
    
    def get_customer_name(self, vehicle_id):
        Booking = Query()
        return self.bookings.get(Booking.vehicle_id == vehicle_id)
    
    def get_financial_metrics(self):
        logs = self.logs.search(Query().transaction_type == "return")
        if not logs:
            return ()
        
        total_revenue = sum(log["revenue"] for log in logs)
        total_additional_costs = sum(log["additional_costs"] for log in logs)
        
        total_maintenance_cost = sum(v["maintenance_cost"] for v in self.vehicles.all())
        avg_mileage = sum(v["current_mileage"] for v in self.vehicles.all()) / len(self.vehicles.all()) if self.vehicles.all() else 0
        
        total_operational_costs = total_maintenance_cost + total_additional_costs
        total_profit = total_revenue - total_operational_costs
        
        return total_revenue, total_operational_costs, total_profit, avg_mileage
    
    def query_update_availability(self, vehicle_id, available):
        self.vehicles.update({"available": available}, doc_ids=[vehicle_id])
    
    def query_update_maintenance_mileage(self, vehicle_id):
        vehicle = self.vehicles.get(doc_id=vehicle_id)
        if vehicle:
            new_maintenance_mileage = vehicle["current_mileage"] + 10000
            self.vehicles.update({"maintenance_mileage": new_maintenance_mileage}, doc_ids=[vehicle_id])
    
    def query_booking(self, vehicle_id, rental_duration, estimated_km, customer_name):
        vehicle = self.vehicles.get(doc_id=vehicle_id)
        if not vehicle or not vehicle["available"]:
            return None
        
        mileage_cost = vehicle["maintenance_cost"] * estimated_km
        duration_cost = vehicle["daily_price"] * rental_duration
        total_estimated_cost = duration_cost + mileage_cost
        
        self.bookings.insert({
            "vehicle_id": vehicle_id,
            "rental_duration": rental_duration,
            "estimated_km": estimated_km,
            "estimated_cost": total_estimated_cost,
            "customer_name": customer_name
        })
        
        self.logs.insert({
            "vehicle_id": vehicle_id,
            "rental_duration": rental_duration,
            "revenue": total_estimated_cost,
            "additional_costs": 0,
            "customer_name": customer_name,
            "transaction_type": "booking"
        })
        
        self.query_update_availability(vehicle_id, False)
        return total_estimated_cost
    
    def query_return(self, vehicle_id, customer_name, actual_km, late_days):
        vehicle = self.vehicles.get(doc_id=vehicle_id)
        if not vehicle:
            return None
        
        maintenance_cost = vehicle["maintenance_cost"] * actual_km
        late_fee = vehicle["daily_price"] * late_days
        total_revenue = maintenance_cost + late_fee
        
        self.logs.insert({
            "vehicle_id": vehicle_id,
            "rental_duration": None,
            "revenue": total_revenue,
            "additional_costs": late_fee,
            "customer_name": customer_name,
            "transaction_type": "return"
        })
        
        self.query_update_availability(vehicle_id, True)
        return total_revenue

    def __del__(self):
        """Ensures the database is closed when the object is deleted"""
        self.database.close()
        print("Database closed.")