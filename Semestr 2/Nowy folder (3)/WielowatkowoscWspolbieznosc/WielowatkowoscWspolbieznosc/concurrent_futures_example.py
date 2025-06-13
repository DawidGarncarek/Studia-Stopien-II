
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time

def zadanie(numer):
    print(f"Zadanie {numer} rozpoczęło pracę.")
    time.sleep(5)
    print(f"Zadanie {numer} zakończyło pracę.")
    return numer

def zadanie2(numer):
    print(f"Zadanie {numer} rozpoczęło pracę.")
    wynik = 0
    for i in range(1,10000000):
        wynik += i**(1/(i))
    print(f"Zadanie {numer} zakończyło pracę.")
    return numer


if __name__ == '__main__':
    #ZADANIE OCZEKIWANIA
    # Tworzenie puli wątków
    print('watki - zadanie')
    with ThreadPoolExecutor(max_workers=3) as executor:
        watki = [executor.submit(zadanie, i) for i in range(5)]
        
        # Oczekiwanie na wyniki zadań
        for watek in watki:
            print(f"Wynik: {watek.result()}")

    print('procesy - zadanie')
    # Tworzenie puli procesow
    with ProcessPoolExecutor(max_workers=3) as executor:
        procesy = [executor.submit(zadanie, i) for i in range(5)]
        
        # Oczekiwanie na wyniki zadań
        for proces in procesy:
            print(f"Wynik: {proces.result()}")

    #ZADANIE OBLICZENIOWE
    print('watki - zadanie2')
    # Tworzenie puli wątków
    with ThreadPoolExecutor(max_workers=3) as executor:
        watki = [executor.submit(zadanie2, i) for i in range(5)]
        
        # Oczekiwanie na wyniki zadań
        for watek in watki:
            print(f"Wynik: {watek.result()}")

    print('procesy - zadanie2')        
    # Tworzenie puli procesow
    with ProcessPoolExecutor(max_workers=3) as executor:
        procesy = [executor.submit(zadanie2, i) for i in range(5)]
        
        # Oczekiwanie na wyniki zadań
        for proces in procesy:
            print(f"Wynik: {proces.result()}")
