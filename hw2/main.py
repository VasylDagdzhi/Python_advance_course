from human import Human
h = Human("Jack", 26, 344.90, True, 300)
h.show_info()


while True:
    print("Welcome to the main menu! Please choose an option.")
    print("1. Get current time")
    print("2. Calculate area of a circle")
    print("3. Find the roots of a quadratic equation")
    print("4. Generate a random number")
    print("5. Convert a temperature")
    print("6. Calculate the circumference of a circle")
    print("7. Reverse a string")
    print("8. Calculate the surface area of a cube")
    print("9. Calculate the volume of a cube")
    print("10. Quit")
    choice = input("Please enter your choice: ")

    if choice == '1':
        get_time()
    elif choice == '2':
        area_circle()
    elif choice == '3':
        quad_roots()
    elif choice == '4':
        random_num()
    elif choice == '5':
        temp_convert()
    elif choice == '6':
        circumference_circle()
    elif choice == '7':