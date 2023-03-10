from person import Person
from house import Home
from time import sleep


class Human(Person):
    salary: int
    header = f"| {'Name:':40} | {'Age:':10} | {'Available money:':15} | {'Has own home:':13} |"
    separator = "-"*len(header)

    def __init__(self, name, age, money, own_house, salary):
        super().__init__(name, age, money, own_house)
        self.salary = salary

    def show_info(self):
        print(self.separator)
        print(self.header)
        print(f"| {self.name:40} | {self.age:10} | {self.available_money:15}$ | {self.has_own_home:13} |")
        print(self.separator)

    def make_money(self):
        self.available_money += self.salary

    def buy_house(self, house: Home):
        if self.has_own_home:
            print(f"{self.name} already has a home!")
            return
        else:
            if self.available_money > house.count_price():
                print(f"{self.name} has enough money.")
                sleep(2)
                self.available_money - house.count_price()
                print(f"Deducted: {house.count_price()} from {self.name} balance.\n"
                      f"Available money left: {self.available_money}$")
                print("Signing documents...")
                sleep(2)
                self.has_own_home = True
                print("House bought!")


