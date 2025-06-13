import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool, cpu_count

def mandelbrot(c, max_iter):
    """
    Funkcja sprawdza, czy liczba c należy do zbioru Mandelbrota.

    Parameters:
        c: Liczba zespolona.
        max_iter: Maksymalna liczba iteracji.

    Returns:
        Liczba iteracji, po której wartość diverguje, lub max_iter.
    """
    z = 0
    for i in range(max_iter):
        z = z**2 + c
        if abs(z) > 2:
            return i
    return max_iter

def mandelbrot_row(y, width, height, x_min, x_max, y_min, y_max, max_iter):
    """
    Oblicza jeden wiersz pikseli zestawu Mandelbrota.

    Parameters:
        y: Indeks wiersza.
        width, height: Wymiary obrazu.
        x_min, x_max, y_min, y_max: Granice przestrzeni zespolonej.
        max_iter: Maksymalna liczba iteracji.

    Returns:
        Lista wartości dla danego wiersza.
    """
    row = []
    for x in range(width):
        real = x_min + (x / width) * (x_max - x_min)
        imag = y_min + (y / height) * (y_max - y_min)
        c = complex(real, imag)
        row.append(mandelbrot(c, max_iter))
    return row

def generate_mandelbrot(width, height, x_min, x_max, y_min, y_max, max_iter):
    """
    Generuje zestaw Mandelbrota z wykorzystaniem wieloprocesowości.

    Parameters:
        width, height: Wymiary obrazu.
        x_min, x_max, y_min, y_max: Granice przestrzeni zespolonej.
        max_iter: Maksymalna liczba iteracji.

    Returns:
        Tablica 2D z wartościami iteracji dla każdego piksela.
    """
    args = [(y, width, height, x_min, x_max, y_min, y_max, max_iter) for y in range(height)]
    with Pool(cpu_count()) as pool:
        rows = pool.starmap(mandelbrot_row, args)
    return np.array(rows)

def plot_mandelbrot(data, x_min, x_max, y_min, y_max):
    """
    Rysuje wykres zbioru Mandelbrota.

    Parameters:
        data: Tablica 2D z wynikami iteracji.
        x_min, x_max, y_min, y_max: Granice przestrzeni zespolonej.
    """
    plt.figure(figsize=(12, 8))
    plt.imshow(data, extent=(x_min, x_max, y_min, y_max), cmap="hot", origin="lower")
    plt.colorbar(label="Liczba iteracji")
    plt.title("Zbiór Mandelbrota")
    plt.xlabel("Część rzeczywista")
    plt.ylabel("Część urojona")
    plt.show()

if __name__ == "__main__":
    # Parametry zestawu Mandelbrota
    width = 1000
    height = 1000
    x_min, x_max = -2.5, 1
    y_min, y_max = -1, 1
    max_iter = 1000

    # Generowanie zestawu Mandelbrota
    mandelbrot_data = generate_mandelbrot(width, height, x_min, x_max, y_min, y_max, max_iter)

    # Rysowanie wykresu
    plot_mandelbrot(mandelbrot_data, x_min, x_max, y_min, y_max)
