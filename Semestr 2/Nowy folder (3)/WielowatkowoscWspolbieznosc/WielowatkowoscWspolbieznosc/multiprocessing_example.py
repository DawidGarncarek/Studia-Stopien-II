import multiprocessing
import time

def zadanie_procesu(numer):
    print(f"Proces {numer} rozpoczął pracę.")
    time.sleep(5)
    print(f"Proces {numer} zakończył pracę.")


# UWAGA!!! wymagane if __name__ == '__main__':
if __name__ == '__main__':
    # Tworzenie i uruchamianie procesów
    procesy = []
    for i in range(3):
        proces = multiprocessing.Process(target=zadanie_procesu, args=(i,))
        procesy.append(proces)
        proces.start()

    # Oczekiwanie na zakończenie pracy procesów
    for proces in procesy:
        proces.join()

    print("Wszystkie procesy zakończyły pracę.")
