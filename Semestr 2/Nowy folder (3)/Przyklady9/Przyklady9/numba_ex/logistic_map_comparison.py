
import numpy as np
import matplotlib.pyplot as plt
import time
from numba import njit, prange
import multiprocessing

# Czysty Python
def logistic_map_python(r_values, n_iter=1000, n_last=100):
    results = []
    for r in r_values:
        x = 0.5  # Początkowa wartość x
        trajectory = []
        for i in range(n_iter):
            x = r * x * (1 - x)
            if i >= n_iter - n_last:  # Zbieraj tylko ostatnie wartości
                trajectory.append((r, x))
        results.extend(trajectory)
    return np.array(results)

# Wieloprocesowość
def logistic_map_worker(r, n_iter, n_last):
    x = 0.5
    trajectory = []
    for i in range(n_iter):
        x = r * x * (1 - x)
        if i >= n_iter - n_last:
            trajectory.append((r, x))
    return trajectory

def logistic_map_multiprocessing(r_values, n_iter=1000, n_last=100):
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    results = pool.starmap(logistic_map_worker, [(r, n_iter, n_last) for r in r_values])
    pool.close()
    pool.join()
    return np.array([item for sublist in results for item in sublist])

# Numba z równoległością
@njit(parallel=True)
def logistic_map_numba_parallel(r_values, n_iter=1000, n_last=100):
    n_r = len(r_values)
    results = np.zeros((n_r, n_last, 2))  # Prealokacja pamięci dla wyników
    for i in prange(n_r):
        r = r_values[i]
        x = 0.5
        for j in range(n_iter):
            x = r * x * (1 - x)
            if j >= n_iter - n_last:
                results[i, j - (n_iter - n_last), 0] = r
                results[i, j - (n_iter - n_last), 1] = x
    return results.reshape(-1, 2)  # Spłaszczenie wyników

# Główna funkcja porównawcza
if __name__ == "__main__":
    r_values = np.linspace(2.5, 4.0, 10000)
    n_iter = 1000
    n_last = 100

    # Obliczenia w czystym Pythonie
    start_time = time.time()
    results_python = logistic_map_python(r_values, n_iter, n_last)
    time_python = time.time() - start_time
    print(f"Czas wykonania:")
    print(f"Czysty Python: {time_python:.4f} s")

    # Obliczenia z wieloprocesowością
    start_time = time.time()
    results_multiprocessing = logistic_map_multiprocessing(r_values, n_iter, n_last)
    time_multiprocessing = time.time() - start_time
    print(f"Wieloprocesowość: {time_multiprocessing:.4f} s")
    
    # Obliczenia z Numba (równoległe)
    start_time = time.time()
    results_numba_parallel = logistic_map_numba_parallel(r_values, n_iter, n_last)
    time_numba_parallel = time.time() - start_time
    print(f"Numba (równoległe): {time_numba_parallel:.4f} s")

    # Wizualizacja mapy logistycznej
    plt.figure(figsize=(12, 6))
    plt.subplot(311)
    plt.scatter(results_python[:, 0], results_python[:, 1], s=0.1, color='blue', label='Python', alpha=0.6)
    #plt.xlabel('r')
    plt.ylabel('x')
    plt.xlim((r_values[0],r_values[-1]))
    plt.subplot(312)
    plt.scatter(results_multiprocessing[:, 0], results_multiprocessing[:, 1], s=0.1, color='orange', label='Multiprocessing', alpha=0.6)
    #plt.xlabel('r')
    plt.ylabel('x')
    plt.xlim((r_values[0],r_values[-1]))
    plt.subplot(313)
    plt.scatter(results_numba_parallel[:, 0], results_numba_parallel[:, 1], s=0.1, color='green', label='Numba Parallel', alpha=0.6)
    plt.xlabel('r')
    plt.ylabel('x')
    plt.xlim((r_values[0],r_values[-1]))
    
    plt.show()

    
    