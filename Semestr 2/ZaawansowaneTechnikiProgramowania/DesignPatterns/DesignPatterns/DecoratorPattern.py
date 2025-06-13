"""W tym przykładzie mamy abstrakcyjną klasę Component, która definiuje metodę operation. 
Klasa ConcreteComponent reprezentuje podstawowy obiekt, który może być dekorowany.
Klasa Decorator jest abstrakcyjnym dekoratorem, który dziedziczy po Component i zawiera odniesienie do komponentu, który dekoruje.
Konkretne dekoratory, takie jak ConcreteDecoratorA i ConcreteDecoratorB, rozszerzają funkcjonalność obiektu, 
dodając nowe operacje i zachowania do jego podstawowej funkcjonalności.
Wzorzec Dekorator pozwala na elastyczne rozszerzanie obiektów, ponieważ możemy dynamicznie dodawać lub usuwać dekoratory w dowolnym momencie. 
Jest to przydatne, gdy chcemy zachować jednolity interfejs i jednocześnie rozszerzać funkcjonalność obiektów bez modyfikowania ich klas."""


# Abstrakcyjna klasa komponentu
class Component:
    def operation(self):
        pass

# Konkretna implementacja komponentu
class ConcreteComponent(Component):
    def operation(self):
        return "Podstawowa operacja"

# Abstrakcyjna klasa dekoratora
class Decorator(Component):
    def __init__(self, component):
        self._component = component

    def operation(self):
        return self._component.operation()

# Konkretny dekorator
class ConcreteDecoratorA(Decorator):
    def operation(self):
        return f"Dodatkowa operacja A, {self._component.operation()}"

# Inny konkretny dekorator
class ConcreteDecoratorB(Decorator):
    def operation(self):
        return f"Dodatkowa operacja B, {self._component.operation()}"

# Użycie wzorca Dekorator
component = ConcreteComponent()
decorator_a = ConcreteDecoratorA(component)
decorator_b = ConcreteDecoratorB(decorator_a)

print(component.operation())
print(decorator_a.operation())
print(decorator_b.operation())
