class Vehicle:
    def __init__(self, id, brand, model, current_mileage, daily_price, maintenance_cost, available=True):
        self.id = id
        self.brand = brand
        self.model = model
        self.current_mileage = current_mileage
        self.maintenance_mileage = current_mileage + 6000
        self.daily_price = daily_price
        self.maintenance_cost = maintenance_cost
        self.available = available