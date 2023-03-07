class Animal:
    name: str
    male: str

    def __init__(self, animal_name, male):
        self.name = animal_name
        if male == "male" or male == "female":
            self.male = male
        else:
            raise ValueError("Incorrect male type.")

    def eat(self):
        print(f"{self.__class__.__name__} {self.name} is eating.")

    def walk(self):
        print(f"{self.__class__.__name__} {self.name} is walking.")

    def sleep(self):
        print(f"Sshhh! {self.__class__.__name__} {self.name} is sleeping.")

    def say_smth(self):
        raise NotImplementedError


class Bear(Animal):
    def say_smth(self):
        print("Beeeeeaaaarrrrr")

    def eat_honey(self):
        print(f"The bear {self.name} is eating honey, yummy!")

    def eat_berries(self):
        print(f"The bear {self.name} is eating wild berries, yummy!")


class Dog(Animal):
    def say_smth(self):
        print("Bark! BArk!")

    def bring_newspaper(self):
        print(f"{self.name} brought the newspaper.")

    def catch_the_ball(self):
        print(f"{self.name} caught the ball!")


class Cat(Animal):
    def say_smth(self):
        print("Meow!")

    def catch_mice(self):
        print(f"The cat {self.name} is hunting mice.")

    def sharpen_claws(self):
        print(f"The cat {self.name} is sharping his claws.")


class Spider(Animal):
    def say_smth(self):
        raise ValueError("Spiders can't talk.")

    def create_nets(self):
        print(f"The spider {self.name} is creating a spider net.")

    def hide(self):
        print(f"The spider {self.name} is hiding.")


class Eagle(Animal):
    def say_smth(self):
        print("EEEEEEEEEEE!!!")

    def catch_rabbit(self):
        print(f"The eagle {self.name} is catching a rabbit. Run, rabbit(Forest), run!")

    def lay_an_egg(self):
        if self.male != "male":
            print(f"The eagle {self.name} is laying an egg.")
        else:
            raise ValueError(f"{self.name} is a male. Males cannot lay eggs!")
