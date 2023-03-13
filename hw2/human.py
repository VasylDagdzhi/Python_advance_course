from person import Person
from house import Home
from time import sleep
from realtor import Realtor


class Human(Person):
    salary: int
    header = f"| {'Name:':40} | {'Age:':4} | {'Available money:':15} | {'Has own home:':13} |"
    separator = "-" * len(header)
    houses = []

    def __init__(
        self, name: str, age: int, money: float, own_house: bool, salary: float
    ):
        if len(name) < 2:
            raise ValueError(
                "The entered name is not valid! It must be at least 2 characters long."
            )
        elif age < 0:
            raise ValueError("The entered age is not valid! It must be above zero.")
        elif money < 0:
            raise ValueError(
                "The entered money amount is not valid! It must be positive to be able to buy a house."
            )
        elif salary < 0:
            raise ValueError(
                "The entered salary amount is not valid! It must be positive."
            )

        super().__init__(name, age, money, own_house)
        self.salary = salary

    def show_info(self):
        print(self.separator)
        print(self.header)
        print(
            f"| {self.name:40} | {self.age:4} | {self.available_money:15}$ | {self.has_own_home.__str__():13} |"
        )
        print(self.separator)

    def make_money(self):
        self.available_money += self.salary

    def buy_house(self, house: Home, realtor: Realtor):
        if self.available_money > house.count_price():
            print(f"{self.name} has enough money.")
            sleep(2)
            realtor.steal_money(house.cost, self)
            self.available_money -= house.count_price()
            print(
                f"Deducted: {house.count_price()} from {self.name} balance.\n"
                f"Available money left: {self.available_money}$"
            )
            print("Signing documents...")
            sleep(2)
            self.has_own_home = True
            self.houses.append(house)
            print("House bought!")
        else:
            print(
                f"Not enough money. You need: {house.count_price() - self.available_money}$. Get to work {self.name}!"
            )

    def show_houses(self):
        if len(self.houses) > 0:
            index = 0
            header = f"| {'Index':10} | {'Area':12} | {'Cost':10}$ |"
            print("-" * len(header))
            print(header)
            for house in self.houses:
                index += 1
                print(
                    f"| {f'[{str(index)}]':10} | {str(house.area):12} | {str(house.cost):10}$ |"
                )
            print("-" * len(header))
        else:
            print("You don't have a house yet.")
