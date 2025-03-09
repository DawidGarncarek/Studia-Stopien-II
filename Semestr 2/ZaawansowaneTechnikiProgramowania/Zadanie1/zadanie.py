from datetime import datetime

class Zadanie:
    def __init__(self, tytul, opis, termin_wykonania):
        self.tytul = tytul
        self.opis = opis
        self.termin_wykonania = datetime.strptime(termin_wykonania, "%Y-%m-%d")
        self.wykonane = False
    
    def oznacz_jako_wykonane(self):
        self.wykonane = True
    
    def __str__(self):
        status = "✔" if self.wykonane else "✘"
        return f"[{status}] {self.tytul} - {self.opis} (Termin: {self.termin_wykonania.date()})"

class ZadaniePriorytetowe(Zadanie):
    def __init__(self, tytul, opis, termin_wykonania, priorytet):
        super().__init__(tytul, opis, termin_wykonania)
        self.priorytet = priorytet
    
    def __str__(self):
        return super().__str__() + f" [Priorytet: {self.priorytet}]"

class ZadanieRegularne(Zadanie):
    def __init__(self, tytul, opis, termin_wykonania, powtarzalnosc):
        super().__init__(tytul, opis, termin_wykonania)
        self.powtarzalnosc = powtarzalnosc
    
    def __str__(self):
        return super().__str__() + f" [Powtarzalność: {self.powtarzalnosc}]"

class ManagerZadan:
    def __init__(self):
        self.zadania = []
    
    def dodaj_zadanie(self, zadanie):
        self.zadania.append(zadanie)
    
    def usun_zadanie(self, tytul):
        self.zadania = [zadanie for zadanie in self.zadania if zadanie.tytul != tytul]
    
    def oznacz_jako_wykonane(self, tytul):
        for zadanie in self.zadania:
            if zadanie.tytul == tytul:
                zadanie.oznacz_jako_wykonane()
    
    def edytuj_zadanie(self, tytul, nowy_tytul, nowy_opis, nowy_termin):
        for zadanie in self.zadania:
            if zadanie.tytul == tytul:
                zadanie.tytul = nowy_tytul
                zadanie.opis = nowy_opis
                zadanie.termin_wykonania = datetime.strptime(nowy_termin, "%Y-%m-%d")
    
    def __contains__(self, tytul):
        return any(zadanie.tytul == tytul for zadanie in self.zadania)
    
    def wyswietl_zadania(self):
        for zadanie in sorted(self.zadania, key=lambda x: x.termin_wykonania):
            print(zadanie)
