import numpy as np
import time
import model
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor

def run_parallel_threads():
    """
    Przeprowadza symulację wielowątkowo dla 100 wartości masy i częstotliwości.
    """
    masses = np.linspace(1, 10, 100)
    frequencies = np.linspace(1, 10, 100)
    results = np.zeros((100, 100))

    start_time = time.time()
    with ProcessPoolExecutor() as executor:
        futures = {(i, j): executor.submit(model.simulate, m, f)
                   for i, m in enumerate(masses) for j, f in enumerate(frequencies)}

        for (i, j), future in futures.items():
            results[i, j] = future.result()
    
    end_time = time.time()
    print(f"Czas obliczeń wielowątkowych: {end_time - start_time:.2f} s")

    plt.figure(figsize=(8, 6))
    plt.pcolormesh(frequencies, masses, results.T, shading='auto')
    plt.colorbar(label="Maksymalne przemieszczenie")
    plt.xlabel("Masa (kg)")
    plt.ylabel("Częstotliwość (Hz)")
    plt.title("Obliczenia wielowątkowe")
    plt.show()
