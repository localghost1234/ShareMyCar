class CarsharingSystem:
    def __init__(self):
        self.vehicles = []
        self.bookings = []
        self.transaction_logs = []

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def book_vehicle(self, vehicle_id, rental_days, estimated_km):
        for vehicle in self.vehicles:
            if vehicle.id == vehicle_id:
                vehicle.available = False
                cost = (vehicle.daily_price * rental_days) + (vehicle.maintenance_cost * estimated_km)
                self.bookings.append({"vehicle_id": vehicle_id, "rental_days": rental_days, "estimated_km": estimated_km, "cost": cost})
                return cost
        return None

    def return_vehicle(self, vehicle_id, actual_km, late_days=0):
        for vehicle in self.vehicles:
            if vehicle.id == vehicle_id:
                vehicle.available = True
                vehicle.mileage += actual_km
                maintenance_cost = vehicle.maintenance_cost * actual_km
                late_fee = 10 * late_days
                cleaning_fee = 20
                total_cost = maintenance_cost + late_fee + cleaning_fee
                self.transaction_logs.append({"vehicle_id": vehicle_id, "actual_km": actual_km, "late_days": late_days, "total_cost": total_cost})
                return total_cost
        return None

    def get_metrics(self):
        total_revenue = sum(booking["cost"] for booking in self.bookings)
        total_costs = sum(log["total_cost"] for log in self.transaction_logs)
        total_profit = total_revenue - total_costs
        return {
            "total_revenue": total_revenue,
            "total_costs": total_costs,
            "total_profit": total_profit,
        }