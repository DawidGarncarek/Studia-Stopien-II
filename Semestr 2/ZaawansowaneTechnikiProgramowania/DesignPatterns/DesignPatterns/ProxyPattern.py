"""W tym przykładzie mamy abstrakcyjną klasę Subject, która definiuje metodę request. 
Klasa RealSubject reprezentuje rzeczywisty obiekt, który implementuje tę metodę.
Klasa Proxy to pełnomocnik, który dziedziczy po Subject i może tworzyć i zarządzać instancją RealSubject. 
Gdy klient wywołuje request na pełnomocniku, ten sprawdza, czy istnieje rzeczywisty obiekt, i jeśli nie, tworzy go, a następnie przekazuje żądanie rzeczywistemu obiektowi.
Wzorzec Pełnomocnika jest przydatny w sytuacjach, gdzie mamy złożone operacje związane z obiektem, które wymagają kontroli dostępu lub dodatkowej logiki. 
Pełnomocnik umożliwia kontrolę nad tymi operacjami, bez konieczności ingerencji w kod rzeczywistego obiektu."""

# Abstrakcyjna klasa podmiotu (Subject)
class Subject:
    def request(self):
        pass
# Rzeczywisty obiekt
class RealSubject(Subject):
    def request(self):
        print("Rzeczywisty obiekt obsługuje żądanie")
# Pełnomocnik (Proxy)
class Proxy(Subject):
    def __init__(self):
        self.real_subject = None

    def request(self):
        if self.real_subject is None:
            self.real_subject = RealSubject()
        self.real_subject.request()

# Użycie wzorca Pełnomocnika
proxy = Proxy()
proxy.request()