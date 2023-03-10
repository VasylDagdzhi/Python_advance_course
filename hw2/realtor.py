from person import Person
from house import Home
from human import Human
import random


class Realtor(Person):
    houses = [Home(40, 2000), Home(100, 10000), Home(400, 80000)]
    discount: int

    def __init__(self, name, age, money, own_house, personal_discount):
        super().__init__(name, age, money, own_house)
        if 5 < personal_discount < 90:
            self.discount = personal_discount
        else:
            raise ValueError("Invalid discount. Discount can be in range 5 - 90%")


class Singleton(Realtor):
    chance_to_steal = 10  # %

    def __init__(self, personal_discount):
        super().__init__("Singleton", 25, 300, False, personal_discount)

    def steal(self, house_cost, victim: Human):
        if random.randint(1, 100) < self.chance_to_steal:
            victim.available_money -= house_cost
            self.available_money += house_cost
            print('HA-HA! Your money was stolen.')
            return True
        else:
            return False

    def show_info_about_houses(self, buyer: Human):
        header = f"| {'Area (m2)':12} | {'Price ($)':12} |"
        print("-" * len(header))
        print(header)
        for house in Realtor.houses:
            print(f"| {str(house.area):12} | {str(house.cost*self.discount/100)} |")
            if self.steal(house.cost, buyer):
                break
            else:
                continue
        print("-" * len(header))
