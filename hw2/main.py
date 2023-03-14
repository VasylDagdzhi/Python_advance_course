from time import sleep
from controller import Controller


Controller.init()

while True:
    Controller.show_menu()
    choice = input("Please enter your choice: ")

    if choice == "1":
        if Controller.customer is not None:
            pass
        else:
            Controller.login_as_customer()
            sleep(1)
    elif choice == "2":
        Controller.show_customer_info()
        sleep(2)
    elif choice == "3":
        Controller.make_money()
        sleep(10)
        Controller.show_customer_info()
    elif choice == "4":
        Controller.show_houses()
        sleep(2)
    elif choice == "5":
        Controller.buy_house()
        sleep(2)
    elif choice == "6":
        Controller.show_client_houses()
        sleep(2)
    elif choice == "10":
        exit(0)
    else:
        pass

