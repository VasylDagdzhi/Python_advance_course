from abc import ABC


class Person(ABC):
    name: str
    age: int
    available_money: float
    has_own_home: bool

    def __init__(self, name, age, money, own_house):
        self.name = name
        self.age = age
        self.available_money = money
        self.has_own_home = own_house
