
import queue
import threading
import time

def producent(kolejka):
    for i in range(5):
        print(f"Producent: dodaję {i} do kolejki")
        kolejka.put(i)
        time.sleep(1)

def konsument(kolejka):
    while True:
        wartosc = kolejka.get()
        print(f"Konsument: odebrałem {wartosc} z kolejki")
        kolejka.task_done()

# Tworzenie kolejki
kolejka = queue.Queue()

# Uruchamianie producenta i konsumenta
producent_watek = threading.Thread(target=producent, args=(kolejka,))
konsument_watek = threading.Thread(target=konsument, args=(kolejka,), daemon=True)

producent_watek.start()
konsument_watek.start()

# Oczekiwanie na zakończenie pracy producenta
producent_watek.join()
kolejka.join()
