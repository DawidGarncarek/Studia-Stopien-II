"""W tym przykładzie mamy abstrakcyjną klasę Animal, która ma metodę speak. 
Następnie mamy dwie konkretne klasy Dog i Cat, które dziedziczą po Animal i implementują metodę speak. 
Klasa AnimalFactory jest odpowiedzialna za tworzenie obiektów Animal na podstawie podanego typu.
Przy użyciu tej fabryki możemy tworzyć różne rodzaje obiektów Animal, podając odpowiedni typ jako argument do create_animal.
Wzorzec Fabryki w Pythonie pozwala na elastyczne tworzenie obiektów różnych klas i izoluje proces tworzenia od kodu klienta,
co ułatwia zarządzanie kodem i wprowadzanie zmian."""

class Animal:
    def speak(self):
        pass
class Dog(Animal):
    def speak(self):
        return "Woof!"
class Cat(Animal):
    def speak(self):
        return "Meow!"
class AnimalFactory:
    def create_animal(self, animal_type):
        if animal_type == "Dog":
            return Dog()
        elif animal_type == "Cat":
            return Cat()
        else:
            return None
# Użycie fabryki
factory = AnimalFactory()
dog = factory.create_animal("Dog")
cat = factory.create_animal("Cat")
print(dog.speak())  # Powinno zwrócić "Woof!"print(cat.speak())  # Powinno zwrócić "Meow!"
print(cat.speak())