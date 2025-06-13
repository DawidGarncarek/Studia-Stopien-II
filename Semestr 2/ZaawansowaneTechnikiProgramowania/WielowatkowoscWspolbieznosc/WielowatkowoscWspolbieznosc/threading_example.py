
import threading
import time

def zadanie_watku(numer):
    print(f"Wątek {numer} rozpoczął pracę.")
    time.sleep(5)
    print(f"Wątek {numer} zakończył pracę.")

# Tworzenie i uruchamianie wątków
watki = []
for i in range(3):
    watek = threading.Thread(target=zadanie_watku, args=(i,))
    watki.append(watek)
    watek.start()

# Oczekiwanie na zakończenie pracy wątków
for watek in watki:
    watek.join()

print("Wszystkie wątki zakończyły pracę.")
