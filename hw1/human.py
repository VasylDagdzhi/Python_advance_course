from animals import Animal, Horse


class Human(Animal):
    def say_smth(self):
        print(f"{self.name} is talking.")

    def hit_with_a_fist(self):
        print(f"{self.name} has just hit his face several times with a fist!")


class Centaur(Human, Horse):
    def say_smth(self):
        print(f"{self.__class__.__name__} {self.name} is talking.")