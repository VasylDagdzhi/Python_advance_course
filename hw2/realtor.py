from house import Home

import random


class Realtor:
    __instance = None

    def __init__(self, name, houses, discount):
        if not Realtor.__instance:
            Realtor.__instance = self
            self.name = name
            self.houses = houses
            self.discount = discount
        else:
            print("Realtor already exists!")

    @staticmethod
    def get_instance():
        if not Realtor.__instance:
            Realtor("Michael", [Home(40, 2000), Home(100, 10000), Home(400, 80000)], 15)
        return Realtor.__instance

    def show_info_about_houses(self, buyer):
        header = f"| {'Area (m2)':12} | {'Price ($)':12} |"
        print("-" * len(header))
        print(header)
        for house in Realtor.__instance.houses:
            print(f"| {str(house.area):12} | {str(house.cost*self.discount/100):12} |")
        print("-" * len(header))

    def provide_discount(self):
        return self.__instance.discount

    @staticmethod
    def steal_money(cost, buyer):
        chance = random.randint(0, 10)
        if chance == 10:
            print(f"{buyer.name}, you have been robbed!")
            buyer.available_money -= cost
            return True
        else:
            return False
