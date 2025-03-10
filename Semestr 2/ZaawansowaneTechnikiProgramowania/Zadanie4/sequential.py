import numpy as np
import time
import model
import matplotlib.pyplot as plt

def run_sequential():
    """
    Przeprowadza symulację sekwencyjnie dla 100 wartości masy i częstotliwości.
    """
    masses = np.linspace(1, 10, 100)
    frequencies = np.linspace(1, 10, 100)
    results = np.zeros((100, 100))

    start_time = time.time()
    for i, m in enumerate(masses):
        for j, f in enumerate(frequencies):
            results[i, j] = model.simulate(m, f)
    end_time = time.time()

    print(f"Czas obliczeń sekwencyjnych: {end_time - start_time:.2f} s")

    plt.figure(figsize=(8, 6))
    plt.pcolormesh(frequencies, masses, results.T, shading='auto')
    plt.colorbar(label="Maksymalne przemieszczenie")
    plt.xlabel("Masa (kg)")
    plt.ylabel("Częstotliwość (Hz)")
    plt.title("Obliczenia sekwencyjne")
    plt.show()
