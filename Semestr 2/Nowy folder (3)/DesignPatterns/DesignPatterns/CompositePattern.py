"""W tym przykładzie mamy abstrakcyjną klasę Component, która definiuje metodę operation. 
Klasa Leaf reprezentuje liść w strukturze kompozytowej i implementuje tę metodę. Klasa Composite reprezentuje kompozyt, 
który może zawierać zarówno liście, jak i inne kompozyty. Implementuje ona metodę operation, która przechodzi przez wszystkie dzieci i zbiera ich wyniki.
Dzięki wzorcowi Kompozytowemu, możemy traktować liście i kompozyty w jednolity sposób. 
To umożliwia tworzenie złożonych hierarchii obiektów i operacje na nich, bez potrzeby szczegółowego rozróżniania liści od kompozytów."""

from abc import ABC, abstractmethod
# Abstrakcyjna klasa komponentu
class Component(ABC):    
    @abstractmethod
    def operation(self):
        pass
# Liść
class Leaf(Component):
    def operation(self):
        return "Liść"
# Kompozyt
class Composite(Component):
    def __init__(self):
        self.children = []

    def add(self, component):
        self.children.append(component)

    def remove(self, component):
        self.children.remove(component)

    def operation(self):
        results = []
        for child in self.children:
            results.append(child.operation())
        return f"Kompozyt({', '.join(results)})"

# Użycie wzorca Kompozytowego
leaf1 = Leaf()
leaf2 = Leaf()

composite = Composite()
composite.add(leaf1)
composite.add(leaf2)

composite2 = Composite()
composite2.add(leaf1)
composite2.add(leaf2)

composite.add(composite2)
print(leaf1.operation())  # Wyświetli: Liść   
print(composite.operation())  # Wyświetli: Kompozyt(Liść, Liść, Kompozyt(Liść, Liść))