from datetime import datetime


class Profile:
    name: str
    last_name: str
    phone_number: str
    address: str
    email: str
    birthday: datetime
    age: int
    sex: str

    def __init__(self, name, lastname, phone_num, address, email, birthday, age, sex):
        self.name = name
        self.last_name = lastname
        self.phone_number = phone_num
        self.address = address
        self.email = email
        self.birthday = birthday
        self.age = age
        self.sex = sex

    def __str__(self):
        return f"Object of {self.__class__} \n -> Name: {self.name} \n -> Last name: {self.last_name} \n" \
               f" -> Phone number: {self.phone_number} \n -> Lives at: {self.address} \n -> E-mail: {self.email} \n" \
               f" -> Born on: {self.birthday.ctime()} \n -> Age: {self.age} \n -> Sex: {self.sex}"


