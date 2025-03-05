class Vehicle:
    def __init__(self, id, brand, model, mileage, daily_price, maintenance_cost, available=True):
        self.id = id
        self.brand = brand
        self.model = model
        self.mileage = mileage
        self.daily_price = daily_price
        self.maintenance_cost = maintenance_cost
        self.available = available