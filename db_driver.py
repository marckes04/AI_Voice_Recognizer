class Car:
    def __init__(self, vin, make, model, year):
        self.vin = vin
        self.make = make
        self.model = model
        self.year = year

class DatabaseDriver:
    def __init__(self):
        self.cars = {"123456": Car("123456", "Toyota", "Corolla", 2024)}

    def get_car_by_vin(self, vin):
        return self.cars.get(vin)

    def create_car(self, vin, make, model, year):
        new_car = Car(vin, make, model, year)
        self.cars[vin] = new_car
        return new_car