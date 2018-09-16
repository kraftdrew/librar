class Human:
    def __init__(self, name, age):
        self.name = name
        self.age = age


class Kovel(Human):
    def show_info(self):
        print("name is:",self.name," age is:",str(self.age))
        #print(f"Name is {self.name} and age {self.age}")

v = Kovel("Vasya", 21)
v.show_info()