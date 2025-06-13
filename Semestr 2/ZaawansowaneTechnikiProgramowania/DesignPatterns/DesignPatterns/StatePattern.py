"""W tym przykładzie mamy abstrakcyjny stan State, który definiuje metodę handle. Następnie mamy konkretne stany, 
ConcreteStateA i ConcreteStateB, które dziedziczą po State i implementują tę metodę.
Klasa Context reprezentuje kontekst, który ma wewnętrzny stan i może zmieniać go za pomocą metody set_state. 
Metoda request wywołuje handle na bieżącym stanie, realizując zachowanie zależnie od ustawionego stanu.
Wzorzec Stanowy pozwala na rozdzielenie logiki stanu od kontekstu, co ułatwia zarządzanie wieloma stanami w obiekcie. 
Jest szczególnie przydatny w przypadku obiektów, które muszą zmieniać swoje zachowanie w zależności od wielu czynników."""

# Abstrakcyjny stan
class State:
    def handle(self):
        pass
# Konkretne stany
class ConcreteStateA(State):
    def handle(self):
        print("Stan A")
class ConcreteStateB(State):
    def handle(self):
        print("Stan B")
# Kontekst
class Context:
    def __init__(self):
        self.state = None

    def set_state(self, state):
        self.state = state

    def request(self):
        if self.state:
            self.state.handle()
        else:
            print("Brak ustawionego stanu")

# Użycie wzorca Stanowego
context = Context()

state_a = ConcreteStateA()
state_b = ConcreteStateB()

context.set_state(state_a)
context.request()

context.set_state(state_b)
context.request()