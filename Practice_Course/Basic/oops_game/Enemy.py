class Enemy:
    def __init__(self,type_of_enemy, health_points, attack_damage):
        print("Welcome to Game")
        self.type_of_enemy = type_of_enemy
        self.health_points = health_points
        self.__attack_damage = attack_damage

    def talk(self):
        print(f'I am {self.type_of_enemy}. Enemy lets talk.')

    def walk(self):
        print(f'I {self.type_of_enemy} walking closer. I have {self.health_points} points.')

    def damage(self):
        print(f'I am going {self.type_of_enemy} attack for to do {self.__attack_damage} damage.')