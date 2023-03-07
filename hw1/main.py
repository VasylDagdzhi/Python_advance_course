from animals import Animal, Bear, Cat, Dog, Spider, Eagle
from human import Centaur
from profile import Profile
from datetime import datetime



print("\n Part 1. \n")

print("Bear class:\n")
b = Bear("Sparky", "male")
b.sleep()
b.walk()
b.eat()
b.eat_honey()
b.eat_berries()
b.say_smth()

print("\nCat class:\n")
c = Cat("Fluffy", "female")
c.sleep()
c.walk()
c.eat()
c.catch_mice()
c.sharpen_claws()
c.say_smth()


print("\nDog class:\n")
d = Dog("Lucky", "male")
d.sleep()
d.walk()
d.eat()
d.bring_newspaper()
d.catch_the_ball()
d.say_smth()

print("\nSpider class:\n")
s = Spider("Crisp", "male")
s.sleep()
s.walk()
s.eat()
s.create_nets()
s.hide()
# s.say_smth()  # uncomment to get the error

print("\nEagle class:\n")
e = Eagle("Prairie", "female")
e1 = Eagle("Muscles", "male")
e.sleep()
e.walk()
e.eat()
e.catch_rabbit()
e.lay_an_egg()
# e1.lay_an_egg() # uncomment to get the error
e.say_smth()

our_animals = [b, c, d, s, e]
for animal in our_animals:
    if isinstance(animal, Animal):
        print(f"{animal.__class__.__name__} is an instance of class Animal")
    else:
        print(f"{animal.__class__.__name__} is not an instance of class Animal")


print("\n Part 1a. \n")

print("Centaur:\n")
cent = Centaur("Kent", "male")
cent.sleep()
cent.walk()
cent.eat()
cent.say_smth()
cent.hit_with_a_fist()
cent.kick_with_both()

print("\n Part 2. \n")

p = Profile("name", "lastname", "210930218038", "Hills ave 91", "name.lastname@gmail.com", datetime.now(), 21, "male")
print(p.__str__())