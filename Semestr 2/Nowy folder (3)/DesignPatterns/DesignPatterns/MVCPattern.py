"""Model reprezentuje dane i logikę biznesową. W tym przypadku ma prostą metodę do ustawiania i pobierania danych.
Widok jest odpowiedzialny za wyświetlanie danych użytkownikowi. W przykładzie jest to prosta klasa, która wyświetla dane w konsoli.
Kontroler jest łącznikiem między modelem a widokiem. Odbiera żądania użytkownika i aktualizuje model, 
a następnie informuje widok o konieczności odświeżenia wyświetlanych danych."""

# Model
class Model:
    def __init__(self):
        self.data = None

    def set_data(self, data):
        self.data = data

    def get_data(self):
        return self.data
# Widok
class View:
    def show_data(self, data):
        print(f"View: {data}")
# Kontroler
class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def update_data(self, data):
        self.model.set_data(data)
        self.view.show_data(self.model.get_data())
# Użycie wzorca MVC
controller = Controller()

controller.update_data("Dane 1")
controller.update_data("Dane 2")