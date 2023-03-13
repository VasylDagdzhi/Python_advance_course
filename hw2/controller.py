from human import Human
from realtor import Realtor
from house import Home


class Controller:
    customer: Human
    realtor: Realtor

    @staticmethod
    def init():
        Controller.realtor = Realtor.get_instance()
        Controller.customer = None

    @staticmethod
    def show_menu():
        print("Welcome to the main menu! Please choose an option.")
        if Controller.customer is not None:
            print("2. Show your information.")
            print("3. Make money.")
            print("4. Show houses.")
            print("5. Buy a house.")
            print("6. Show your houses.")
        else:
            print("1. Log in as a customer.")
        print("10. Quit")

    @staticmethod
    def login_as_customer():
        try:
            name = str(input("Please enter your name: "))
            age = int(input("Please enter your age: "))
            money = float(input("Please enter your money amount: "))
            own_house = bool(
                int(input("Please enter 1 if you have a home or 0 if you don't: "))
            )
            if own_house:
                house_area = int(input("Please enter the house area that you own: "))
                house_cost = float(input("Please enter the house cost that you own: "))
                Controller.customer.houses.append(Home(house_area, house_cost))
            salary = float(input("Please enter your salary: "))
            Controller.customer = Human(name, age, money, own_house, salary)
        except ValueError as e:
            print(e)

    @staticmethod
    def show_customer_info():
        Controller.customer.show_info()

    @staticmethod
    def make_money():
        Controller.customer.make_money()

    @staticmethod
    def show_houses():
        Controller.realtor.show_info_about_houses(Controller.customer)

    @staticmethod
    def select_house():
        index = 0
        for house in Controller.realtor.houses:
            index += 1
            print(f"[{index}] \t Area: {house.area}m2 \t Cost: {house.cost}$.")
        print(index)
        try:
            selection = int(
                input("Please enter the house index that you want to buy: ")
            )
        except ValueError as e:
            print(e)

        if selection > index:
            raise ValueError("Invalid input. House index out of range!")
        else:
            Controller.customer.buy_house(
                Controller.realtor.houses[selection - 1], Controller.realtor
            )

    @staticmethod
    def buy_house():
        Controller.select_house()

    @staticmethod
    def show_client_houses():
        Controller.customer.show_houses()
