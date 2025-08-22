# simple class 

class Car:
    def __init__(self,brand, model):
        self.__brand = brand
        self.model = model

    def hello(self):
        print("welcome to car class")
    
    def get_brand(self):
        return self.__brand + '!!'
    
    def full_car(self):
        return f"{self.__brand} is brand name and name is {self.model}"
    
    def flue_type(self):
        return "Petrol or Diesel"
    


class ElectricCar(Car):
    def __init__(self,brand, model, battery_size):
         super().__init__(brand,model)
         self.battery_size = battery_size
    def flue_type(self):
        return "Electric Charge"





my_tesla = ElectricCar("Tesla", "Model s", "85Kwh")

# print(my_tesla.model)
# print(my_tesla.full_car())

print(my_tesla.flue_type())
        
# print(my_tesla.__brand)
# print(my_tesla.get_brand())

my_car = Car("Maruti", "Swift")

print(my_car.flue_type())

# print(my_car.brand)
# print(my_car.model)
# print(my_car.full_car())

# my_car_tata = Car("Tata", "Punch")

# print(my_car_tata.brand)
# print(my_car_tata.model)
# print(my_car_tata.full_car())


# encapsulation make variable private like brand. hide details inside class 

# polymorphism one method different form.