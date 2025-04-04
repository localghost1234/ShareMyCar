from src.misc.constants import DB_NAME
import pickle
import os

def load_data():
    if os.path.exists(DB_NAME):
        with open(DB_NAME, "rb") as f:
            return pickle.load(f)
    return {"vehicles": [], "bookings": [], "logs": []}

def save_data(data):
    with open(DB_NAME, "wb") as f:
        pickle.dump(data, f)

class System:
    def __init__(self):
        self.data = load_data()
    
    def add_vehicle(self, brand, model, mileage, daily_price, maintenance_cost):
        vehicle = {
            "id": len(self.data["vehicles"]) + 1,
            "brand": brand,
            "model": model,
            "current_mileage": mileage,
            "daily_price": daily_price,
            "maintenance_cost": maintenance_cost,
            "maintenance_mileage": mileage + 10000,
            "available": True
        }
        self.data["vehicles"].append(vehicle)
        save_data(self.data)
    
    def get_all_vehicles(self):
        return self.data["vehicles"]
    
    def get_all_bookings(self):
        return self.data["bookings"]
    
    def get_all_logs(self):
        return self.data["logs"]
    
    def get_vehicles_requiring_maintenance(self):
        return [v for v in self.data["vehicles"] if v["current_mileage"] >= v["maintenance_mileage"]]
    
    def get_unavailable_vehicles(self):
        return [v for v in self.data["vehicles"] if not v["available"]]
    
    def get_table_column(self, table_name, column_name):
        return [record[column_name] for record in self.data.get(table_name, []) if column_name in record]
    
    def get_customer_name(self, vehicle_id):
        result = next((b for b in self.data["bookings"] if b["vehicle_id"] == vehicle_id), None)
        return result["customer_name"] if result else "Unknown Customer"
    
    def get_financial_metrics(self):
        logs = [log for log in self.data["logs"] if log["transaction_type"] == "return"]
        if not logs:
            return ()
        
        total_revenue = sum(log["revenue"] for log in logs)
        total_additional_costs = sum(log["additional_costs"] for log in logs)
        total_maintenance_cost = sum(v["maintenance_cost"] for v in self.data["vehicles"])
        avg_mileage = sum(v["current_mileage"] for v in self.data["vehicles"]) / len(self.data["vehicles"]) if self.data["vehicles"] else 0
        
        total_operational_costs = total_maintenance_cost + total_additional_costs
        total_profit = total_revenue - total_operational_costs
        
        return total_revenue, total_operational_costs, total_profit, avg_mileage
    
    def query_update_availability(self, vehicle_id, available):
        for v in self.data["vehicles"]:
            if v["id"] == vehicle_id:
                v["available"] = available
                save_data(self.data)
                return True
        return False
    
    def query_update_maintenance_mileage(self, vehicle_id):
        for v in self.data["vehicles"]:
            if v["id"] == vehicle_id:
                v["maintenance_mileage"] = v["current_mileage"] + 10000
                save_data(self.data)
                return True
        return False
    
    def query_booking(self, vehicle_id, rental_duration, estimated_km, customer_name):
        vehicle = next((v for v in self.data["vehicles"] if v["id"] == vehicle_id and v["available"]), None)
        if not vehicle:
            return None
        
        mileage_cost = vehicle["maintenance_cost"] * estimated_km
        duration_cost = vehicle["daily_price"] * rental_duration
        total_estimated_cost = float(duration_cost + mileage_cost)
        
        self.data["bookings"].append({
            "id": len(self.data["bookings"]) + 1,
            "vehicle_id": vehicle_id,
            "rental_duration": rental_duration,
            "estimated_km": estimated_km,
            "estimated_cost": total_estimated_cost,
            "customer_name": customer_name
        })
        
        self.data["logs"].append({
            "id": len(self.data["logs"]) + 1,
            "vehicle_id": vehicle_id,
            "rental_duration": rental_duration,
            "revenue": total_estimated_cost,
            "additional_costs": 0.0,
            "customer_name": customer_name,
            "transaction_type": "booking"
        })
        
        self.query_update_availability(vehicle_id, False)
        return total_estimated_cost
    
    def query_return(self, vehicle_id, customer_name, actual_km, late_days):
        vehicle = next((v for v in self.data["vehicles"] if v["id"] == vehicle_id), None)
        if not vehicle:
            return None
        
        original_booking = next((b for b in self.data["bookings"] if b["vehicle_id"] == vehicle_id), None)
        if not original_booking:
            return None
        
        self.data["bookings"] = [b for b in self.data["bookings"] if b["vehicle_id"] != vehicle_id]
        rental_duration = original_booking["rental_duration"] + late_days
        vehicle["current_mileage"] += actual_km
        maintenance_cost = vehicle["maintenance_cost"] * actual_km
        late_fee = vehicle["daily_price"] * late_days
        total_revenue = maintenance_cost + late_fee
        
        self.data["logs"].append({
            "id": len(self.data["logs"]) + 1,
            "vehicle_id": vehicle_id,
            "rental_duration": rental_duration,
            "revenue": total_revenue,
            "additional_costs": late_fee,
            "customer_name": customer_name,
            "transaction_type": "return"
        })
        
        self.query_update_availability(vehicle_id, True)
        return total_revenue
