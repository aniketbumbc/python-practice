# simple class 

class Car:
    def __init__(self,brand, model):
        self.brand = brand
        self.model = model

    def hello(self):
        print("welcome to car class")
    
    def full_car(self):
        return f"{self.brand} is brand name and name is {self.model}"
    


class ElectricCar(Car):
    def __init__(self,brand, model, battery_size):
         super().__init__(brand,model)
         self.battery_size = battery_size





my_tesla = ElectricCar("Tesla", "Model s", "85Kwh")

print(my_tesla.model)
print(my_tesla.full_car())
        

# my_car = Car("Maruti", "Swift")

# print(my_car.brand)
# print(my_car.model)
# print(my_car.full_car())

# my_car_tata = Car("Tata", "Punch")

# print(my_car_tata.brand)
# print(my_car_tata.model)
# print(my_car_tata.full_car())