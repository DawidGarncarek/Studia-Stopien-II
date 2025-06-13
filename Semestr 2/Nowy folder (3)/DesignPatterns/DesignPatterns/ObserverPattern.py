"""W tym przykładzie mamy klasę Subject, która reprezentuje podmiot, który może być obserwowany. 
Klasa ta ma metody attach do dołączania obserwatorów, detach do usuwania obserwatorów i notify do powiadamiania obserwatorów o zmianach.
Mamy również klasę Observer, która jest klasą bazową dla obserwatorów. Każdy konkretny obserwator dziedziczy po tej klasie i implementuje metodę update,
która zostanie wywołana, gdy podmiot będzie informował obserwatorów o zmianach.
W przykładzie tworzymy konkretnego obserwatora ConcreteObserver i przypisujemy go do podmiotu. 
Następnie, gdy podmiot informuje obserwatorów za pomocą notify, każdy obserwator reaguje na zmiany, wywołując swoją metodę update.
Wzorzec Obserwator w Pythonie umożliwia elastyczną implementację mechanizmu powiadamiania o zmianach,
gdzie podmioty i obserwatorzy są oddzielone, co ułatwia rozszerzalność i zarządzanie kodem."""

class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, message):
        for observer in self._observers:
            observer.update(message)
class Observer:
    def update(self, message):
        pass
class ConcreteObserver(Observer):
    def update(self, message):
        print(f"Received message: {message}")
# Użycie wzorca Obserwator
subject = Subject()

observer1 = ConcreteObserver()
observer2 = ConcreteObserver()

subject.attach(observer1)
subject.attach(observer2)

subject.notify("Hello, observers!")

subject.detach(observer2)

subject.notify("Observers, are you there?")