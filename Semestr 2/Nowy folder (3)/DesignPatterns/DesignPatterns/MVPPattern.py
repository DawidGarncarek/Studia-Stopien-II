"""Model reprezentuje dane i logikę biznesową, podobnie jak w przypadku wzorca MVC.
Widok jest odpowiedzialny za wyświetlanie danych, ale jest bardziej pasywny niż widok w MVC. 
W przypadku MVP widok wie o prezenterze i umożliwia prezenterowi dostęp do niego. Jednak to prezenter kontroluje, co i kiedy jest wyświetlane.
Prezenter zajmuje się komunikacją między modelem a widokiem. Prezenter odbiera żądania użytkownika i aktualizuje model oraz widok."""

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
    def set_presenter(self, presenter):
        self.presenter = presenter

    def show_data(self, data):
        print(f"View: {data}")
# Prezenter
class Presenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_presenter(self)

    def update_data(self, data):
        self.model.set_data(data)
        self.view.show_data(self.model.get_data())
# Użycie wzorca MVP
model = Model()
view = View()
presenter = Presenter(model, view)

presenter.update_data("Dane 1")
presenter.update_data("Dane 2")