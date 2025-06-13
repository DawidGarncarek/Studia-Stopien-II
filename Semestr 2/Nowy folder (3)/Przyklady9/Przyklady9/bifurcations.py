import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool, cpu_count

def logistic_map(r, x, n):
    """Oblicza iteracje mapy logistycznej."""
    for _ in range(n):
        x = r * x * (1 - x)
    return x

def bifurcation(r_min, r_max, num_r, num_iter, num_last):
    """
    Oblicza punkty bifurkacji dla zakresu parametrów r.
    """
    r_values = np.linspace(r_min, r_max, num_r)
    x = 0.5  # początkowe x
    results = []
    for r in r_values:
        # Przepal iteracje początkowe
        for _ in range(num_iter - num_last):
            x = logistic_map(r, x, 1)
        # Zapisz ostatnie wartości
        for _ in range(num_last):
            x = logistic_map(r, x, 1)
            results.append((r, x))
    return results

def parallel_bifurcation(r_min, r_max, num_r, num_iter, num_last):
    """
    Rozdziela obliczenia bifurkacji między procesy.
    """
    num_processes = cpu_count()
    r_split = np.array_split(np.linspace(r_min, r_max, num_r), num_processes)
    args = [(r[0], r[-1], len(r), num_iter, num_last) for r in r_split]
    
    with Pool(processes=num_processes) as pool:
        results = pool.starmap(bifurcation, args)
    
    # Połącz wyniki z wszystkich procesów
    merged_results = [item for sublist in results for item in sublist]
    return merged_results

def plot_bifurcation(data):
    """
    Rysuje mapę logistyczną na podstawie danych.
    """
    r_values, x_values = zip(*data)
    plt.figure(figsize=(12, 8))
    plt.scatter(r_values, x_values, s=0.1, color='black')
    plt.title("Mapa logistyczna z bifurkacjami")
    plt.xlabel("r")
    plt.ylabel("x")
    plt.show()

if __name__ == "__main__":
    # Parametry bifurkacji
    r_min = 2.5
    r_max = 4.0
    num_r = 10000  # liczba punktów r
    num_iter = 1000  # liczba iteracji
    num_last = 100  # liczba ostatnich wartości do zapisania

    # Oblicz punkty bifurkacji
    bifurcation_data = parallel_bifurcation(r_min, r_max, num_r, num_iter, num_last)

    # Rysuj wykres
    plot_bifurcation(bifurcation_data)
