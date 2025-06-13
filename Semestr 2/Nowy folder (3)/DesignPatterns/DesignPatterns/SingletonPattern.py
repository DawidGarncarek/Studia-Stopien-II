"""W tej implementacji wzorca Singleton używamy metody __new__, 
która jest wywoływana przed __init__, aby sprawdzić, czy istnieje już instancja klasy. 
Jeśli instancja nie istnieje, tworzymy nową, inicjalizujemy ją i zwracamy. 
W przeciwnym razie zwracamy istniejącą instancję.
Dzięki temu wzorzecowi Singleton możemy mieć pewność, 
że w naszym programie będzie istnieć tylko jedna instancja klasy, 
co jest przydatne w wielu przypadkach, 
gdzie chcemy uniknąć nadmiernego zużycia zasobów lub konfliktów wynikających z wielu instancji tej samej klasy."""

class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        # Inicjalizacja instancji, jeśli to konieczne
        pass
# Użycie Singleton
singleton_instance1 = Singleton()
singleton_instance2 = Singleton()
print(singleton_instance1 is singleton_instance2)  # Powinno zwrócić True
print(singleton_instance1)
print(singleton_instance2)
